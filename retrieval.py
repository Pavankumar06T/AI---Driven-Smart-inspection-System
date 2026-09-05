"""
Given an ExtractionOutput, return the compliance rules that are
plausibly relevant — combining structured pre-filtering (applies_when)
with semantic search (embeddings) as a fallback/booster.
"""

import ast
import chromadb
from chromadb.utils import embedding_functions
from models import ExtractionOutput

client = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_collection(
    name="compliance_rules",
    embedding_function=embedding_fn,
)


# LIMITATION: uses first-match by name. On multi-row/multi-worker documents, only the first matching row is checked per rule. Fine for establishment-level fields (registration_number, safety_committee_record) but under-checks per-worker fields (overtime_hours, gross_wages, etc.) on documents with multiple workers. Not fixed for hackathon scope — documented as a known next step.
def _get_field(extraction: ExtractionOutput, name: str):
    return next((field for field in extraction.fields if field.name == name), None)


def _as_number(value):
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _as_bool(value):
    return str(value).strip().lower() in {"true", "yes", "y", "1"}


def _matches(value, expected) -> bool:
    if expected == "*":
        return True
    if isinstance(expected, list):
        return value in expected
    return value == expected


def _passes_structured_filter(applies_when: dict, extraction: ExtractionOutput) -> bool:
    """Check whether the establishment profile satisfies a rule's
    structured preconditions. Returns True if the rule *could* apply
    (fields missing needed to decide => treated as 'possibly applies',
    letting the reasoning engine's cannot_determine logic handle it)."""
    profile = extraction.establishment_profile

    if "min_headcount_hazardous" in applies_when:
        headcount = profile.headcount
        hazardous_field = _get_field(extraction, "hazardous_process_flag")
        hazardous = None if hazardous_field is None else _as_bool(hazardous_field.value)
        if headcount is None or hazardous is None:
            return True
        if headcount >= applies_when.get("min_headcount", float("inf")):
            return True
        return hazardous and headcount >= applies_when["min_headcount_hazardous"]

    for key, threshold in applies_when.items():
        if key in ("state", "sector"):
            if not _matches(getattr(profile, key), threshold):
                return False
            continue
        if key == "min_headcount":
            if profile.headcount is None:
                continue
            if profile.headcount < threshold:
                return False
        if key in ("min_contract_labour", "min_ismw_count"):
            field_name = {"min_contract_labour": "contract_labour_count", "min_ismw_count": "ismw_count"}[key]
            field = _get_field(extraction, field_name)
            count = None if field is None else _as_number(field.value)
            if count is not None and count < threshold:
                return False
    return True


def retrieve_relevant_rules(extraction: ExtractionOutput, top_k: int = 8) -> list[dict]:
    profile = extraction.establishment_profile

    field_names = [f.name for f in extraction.fields]
    query_text = (
        f"Sector: {profile.sector}. State: {profile.state}. "
        f"Extracted fields present: {', '.join(field_names)}."
    )

    results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
    )

    candidate_rules = []
    for metadata in results["metadatas"][0]:
        applies_when = ast.literal_eval(metadata["applies_when_json"])
        if _passes_structured_filter(applies_when, extraction):
            candidate_rules.append(metadata)

    return candidate_rules
"""
Given an ExtractionOutput, return the compliance rules that are
plausibly relevant — combining structured pre-filtering (applies_when)
with semantic search (embeddings) as a fallback/booster.
"""

import ast
from models import ExtractionOutput
from rules_data import RULES

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
    """Check whether the establishment profile satisfies a rule's structured preconditions."""
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
    field_names_set = {f.name for f in extraction.fields}

    # Attempt ChromaDB retrieval if installed and initialized
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        client = chromadb.PersistentClient(path="./chroma_db")
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        collection = client.get_collection(
            name="compliance_rules",
            embedding_function=embedding_fn,
        )
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
        if candidate_rules:
            return candidate_rules
    except Exception:
        pass

    # Lightweight Rule Matching (Fast, zero PyTorch/ChromaDB memory overhead)
    candidate_rules = []
    for rule in RULES:
        if not _passes_structured_filter(rule.applies_when, extraction):
            continue

        rule_deps = set(rule.field_dependencies)
        overlap = len(field_names_set.intersection(rule_deps))

        metadata = {
            "check_id": rule.check_id,
            "scenario": rule.scenario,
            "title": rule.title,
            "code": rule.code,
            "section": rule.section,
            "severity": rule.severity,
            "violation_type": rule.violation_type,
            "applies_when_json": str(rule.applies_when),
            "field_dependencies_csv": ",".join(rule.field_dependencies),
            "_score": overlap
        }
        candidate_rules.append(metadata)

    # Sort candidates by relevance overlap and severity
    candidate_rules.sort(key=lambda r: (r["_score"], r["severity"]), reverse=True)
    return candidate_rules[:top_k]
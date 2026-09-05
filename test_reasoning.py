from models import ExtractionOutput
from retrieval import retrieve_relevant_rules
from reasoning import generate_findings

sample = {
    "document_id": "doc_001",
    "establishment_profile": {
        "state": "Tamil Nadu", "sector": "Manufacturing",
        "headcount": 45, "contractor_involved": True, "worker_type": "contract"
    },
    "document_quality": {"overall_score": 0.82, "issues": []},
    "fields": [
        {"field_id": "f1", "name": "monthly_wage", "value": "6000",
         "evidence": {"page": 1, "bbox": [10, 20, 100, 15], "text_snippet": "Wage: 6000"},
         "extraction_confidence": "high"},
        {"field_id": "f2", "name": "worker_skill_category", "value": "unskilled",
         "evidence": {"page": 1, "bbox": [10, 40, 100, 15], "text_snippet": "Category: unskilled"},
         "extraction_confidence": "high"},
        {"field_id": "f3", "name": "state", "value": "Tamil Nadu",
         "evidence": {"page": 1, "bbox": [10, 60, 100, 15], "text_snippet": "State: TN"},
         "extraction_confidence": "high"},
    ]
}

extraction = ExtractionOutput(**sample)
rules = retrieve_relevant_rules(extraction)
findings = generate_findings(extraction, rules)

for f in findings:
    print(f"[{f.type}] {f.finding_id} — {f.explanation}")
    if f.citation:
        print(f"   citation: {f.citation.code}, {f.citation.section} (confidence: {f.confidence})")
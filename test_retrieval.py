from models import ExtractionOutput
from retrieval import retrieve_relevant_rules

sample = {
    "document_id": "doc_001",
    "establishment_profile": {
        "state": "Tamil Nadu",
        "sector": "Manufacturing",
        "headcount": 45,
        "contractor_involved": True,
        "worker_type": "contract"
    },
    "document_quality": {"overall_score": 0.82, "issues": []},
    "fields": [
        {
            "field_id": "f1",
            "name": "monthly_wage",
            "value": "8000",
            "evidence": {"page": 1, "bbox": [10, 20, 100, 15], "text_snippet": "Wage: 8000"},
            "extraction_confidence": "high"
        },
        {
            "field_id": "f2",
            "name": "safety_committee_record",
            "value": "not found",
            "evidence": {"page": 2, "bbox": [0, 0, 0, 0], "text_snippet": ""},
            "extraction_confidence": "low"
        }
    ]
}

extraction = ExtractionOutput(**sample)
rules = retrieve_relevant_rules(extraction)

for r in rules:
    print(f"{r['check_id']} — {r['title']} (severity {r['severity']})")
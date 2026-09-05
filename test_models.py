from models import ExtractionOutput

sample = {
    "document_id": "doc_001",
    "establishment_profile": {
        "state": "Tamil Nadu",
        "sector": "Manufacturing",
        "headcount": 45,
        "contractor_involved": True,
        "worker_type": "contract"
    },
    "document_quality": {"overall_score": 0.82, "issues": ["slightly blurred page 2"]},
    "fields": [
        {
            "field_id": "f1",
            "name": "monthly_wage",
            "value": "8000",
            "evidence": {"page": 1, "bbox": [10, 20, 100, 15], "text_snippet": "Wage: 8000"},
            "extraction_confidence": "high"
        }
    ]
}

parsed = ExtractionOutput(**sample)
print(parsed.establishment_profile.state)
print("Valid")
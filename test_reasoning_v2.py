from models import ExtractionOutput
from retrieval import retrieve_relevant_rules
from reasoning import generate_findings

sample = {
    "document_id": "doc_002",
    "establishment_profile": {
        "state": "Tamil Nadu",
        "sector": "Manufacturing",
        "headcount": 45,
        "contractor_involved": True,
        "worker_type": "contract"
    },
    "document_quality": {"overall_score": 0.78, "issues": ["page 3 slightly blurred"]},
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

        {"field_id": "f4", "name": "overtime_hours", "value": "10",
         "evidence": {"page": 2, "bbox": [10, 20, 100, 15], "text_snippet": "OT hours: 10"},
         "extraction_confidence": "high"},
        {"field_id": "f5", "name": "overtime_pay", "value": "600",
         "evidence": {"page": 2, "bbox": [10, 40, 100, 15], "text_snippet": "OT pay: 600"},
         "extraction_confidence": "high"},
        {"field_id": "f6", "name": "normal_wage_rate", "value": "100",
         "evidence": {"page": 2, "bbox": [10, 60, 100, 15], "text_snippet": "Normal rate: 100/hr"},
         "extraction_confidence": "high"},

        {"field_id": "f7", "name": "gross_wages", "value": "10000",
         "evidence": {"page": 2, "bbox": [10, 80, 100, 15], "text_snippet": "Gross: 10000"},
         "extraction_confidence": "high"},
        {"field_id": "f8", "name": "total_deductions", "value": "2000",
         "evidence": {"page": 2, "bbox": [10, 100, 100, 15], "text_snippet": "Deductions: 2000"},
         "extraction_confidence": "high"},

        {"field_id": "f9", "name": "employee_monthly_wage", "value": "6000",
         "evidence": {"page": 3, "bbox": [10, 20, 100, 15], "text_snippet": "Monthly wage: 6000"},
         "extraction_confidence": "medium"},

        {"field_id": "f10", "name": "daily_working_hours", "value": "10",
         "evidence": {"page": 3, "bbox": [10, 40, 100, 15], "text_snippet": "Daily hours: 10"},
         "extraction_confidence": "high"},
        {"field_id": "f11", "name": "weekly_working_hours", "value": "60",
         "evidence": {"page": 3, "bbox": [10, 60, 100, 15], "text_snippet": "Weekly hours: 60"},
         "extraction_confidence": "high"},
    ]
}

extraction = ExtractionOutput(**sample)
rules = retrieve_relevant_rules(extraction)
findings = generate_findings(extraction, rules)

print(f"\n{'='*70}")
print(f"Retrieved {len(rules)} candidate rules, produced {len(findings)} findings")
print(f"{'='*70}\n")

for f in findings:
    print(f"[{f.type.upper()}] {f.finding_id}")
    print(f"   {f.explanation}")
    if f.citation:
        print(f"   citation: {f.citation.code}, {f.citation.section} (confidence: {f.confidence})")
    if f.reason:
        print(f"   reason: {f.reason}")
    print()
import pytest
from pydantic import ValidationError
from models import ExtractionOutput, EstablishmentProfile, DocumentQuality, ExtractedField, Evidence

def test_single_field_extraction_output_valid():
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
                "evidence": {"page": 1, "bbox": [10.0, 20.0, 100.0, 15.0], "text_snippet": "Wage: 8000"},
                "extraction_confidence": "high"
            }
        ]
    }
    parsed = ExtractionOutput(**sample)
    assert parsed.document_id == "doc_001"
    assert parsed.establishment_profile.state == "Tamil Nadu"

def test_repeated_field_names_with_unique_field_ids_valid():
    """ExtractionOutput with multiple fields sharing the same name but unique field_ids must PASS."""
    sample = {
        "document_id": "doc_wage_multi_row",
        "establishment_profile": {
            "state": "Maharashtra",
            "sector": "Textile Factory",
            "headcount": 85
        },
        "document_quality": {"overall_score": 0.75, "issues": []},
        "fields": [
            {
                "field_id": "f1",
                "name": "overtime_hours",
                "value": "14.5 hrs",
                "evidence": {"page": 1, "bbox": [10.0, 10.0, 20.0, 5.0], "text_snippet": "OT 14.5"},
                "extraction_confidence": "medium"
            },
            {
                "field_id": "f2",
                "name": "overtime_hours",
                "value": "8.0 hrs",
                "evidence": {"page": 1, "bbox": [10.0, 20.0, 20.0, 5.0], "text_snippet": "OT 8.0"},
                "extraction_confidence": "medium"
            }
        ]
    }
    parsed = ExtractionOutput(**sample)
    assert len(parsed.fields) == 2
    assert parsed.fields[0].name == parsed.fields[1].name == "overtime_hours"
    assert parsed.fields[0].field_id == "f1"
    assert parsed.fields[1].field_id == "f2"

def test_duplicate_field_ids_raises_validation_error():
    """Duplicate field_id values must fail validation."""
    sample = {
        "document_id": "doc_duplicate_field_ids",
        "establishment_profile": {"state": "Delhi", "sector": "Service"},
        "document_quality": {"overall_score": 0.90, "issues": []},
        "fields": [
            {
                "field_id": "f1",
                "name": "overtime_hours",
                "value": "10 hrs",
                "evidence": {"page": 1, "bbox": [10.0, 10.0, 20.0, 5.0], "text_snippet": "10"},
                "extraction_confidence": "high"
            },
            {
                "field_id": "f1",
                "name": "gross_wages",
                "value": "15000",
                "evidence": {"page": 1, "bbox": [10.0, 20.0, 20.0, 5.0], "text_snippet": "15000"},
                "extraction_confidence": "high"
            }
        ]
    }
    with pytest.raises(ValidationError) as excinfo:
        ExtractionOutput(**sample)
    assert "field_id values must be unique" in str(excinfo.value)
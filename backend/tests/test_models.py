import pytest
from pydantic import ValidationError
from app.models import (
    EstablishmentProfile,
    Evidence,
    ExtractedField,
    DocumentQuality,
    ExtractionOutput
)

def test_establishment_profile_valid():
    profile = EstablishmentProfile(
        state="Maharashtra",
        sector="Factory",
        headcount=150,
        contractor_involved=True,
        worker_type="Skilled"
    )
    assert profile.state == "Maharashtra"
    assert profile.headcount == 150
    assert profile.contractor_involved is True

def test_evidence_bbox_validation():
    # Valid evidence
    ev = Evidence(page=1, bbox=[10.0, 20.0, 30.0, 40.0], text_snippet="Sample Snippet")
    assert ev.page == 1
    assert len(ev.bbox) == 4

    # Invalid bbox length (must be 4 elements)
    with pytest.raises(ValidationError):
        Evidence(page=1, bbox=[10.0, 20.0], text_snippet="Invalid")

def test_extracted_field_confidence_literal():
    field = ExtractedField(
        field_id="f1",
        name="monthly_wage",
        value="18500",
        evidence=Evidence(page=1, bbox=[10.0, 10.0, 20.0, 5.0], text_snippet="Wage 18500"),
        extraction_confidence="high"
    )
    assert field.extraction_confidence == "high"

    # Invalid confidence value
    with pytest.raises(ValidationError):
        ExtractedField(
            field_id="f2",
            name="monthly_wage",
            value="18500",
            evidence=Evidence(page=1, bbox=[10.0, 10.0, 20.0, 5.0], text_snippet="Wage 18500"),
            extraction_confidence="unknown_value" # type: ignore
        )

def test_full_extraction_output_schema():
    output = ExtractionOutput(
        document_id="doc_test123",
        establishment_profile=EstablishmentProfile(
            state="Karnataka",
            sector="Construction"
        ),
        document_quality=DocumentQuality(
            overall_score=0.88,
            issues=["Minor handwriting blur on line 4"]
        ),
        fields=[
            ExtractedField(
                field_id="f1",
                name="registration_number",
                value="REG-9912",
                evidence=Evidence(page=1, bbox=[5.0, 5.0, 50.0, 10.0], text_snippet="REG-9912"),
                extraction_confidence="high"
            )
        ]
    )
    data = output.model_dump()
    assert data["document_id"] == "doc_test123"
    assert data["document_quality"]["overall_score"] == 0.88
    assert len(data["fields"]) == 1
    assert data["fields"][0]["field_id"] == "f1"


def test_repeated_field_names_allowed():
    """Verify that multiple fields sharing the same name but unique field_ids pass validation."""
    output = ExtractionOutput(
        document_id="doc_multi_row",
        establishment_profile=EstablishmentProfile(
            state="Maharashtra",
            sector="Factory"
        ),
        document_quality=DocumentQuality(
            overall_score=0.85,
            issues=[]
        ),
        fields=[
            ExtractedField(
                field_id="f1",
                name="overtime_hours",
                value="10.0 hrs",
                evidence=Evidence(page=1, bbox=[10.0, 10.0, 20.0, 5.0], text_snippet="10.0 hrs"),
                extraction_confidence="high"
            ),
            ExtractedField(
                field_id="f2",
                name="overtime_hours",
                value="8.0 hrs",
                evidence=Evidence(page=1, bbox=[10.0, 20.0, 20.0, 5.0], text_snippet="8.0 hrs"),
                extraction_confidence="high"
            )
        ]
    )
    assert len(output.fields) == 2
    assert output.fields[0].name == output.fields[1].name == "overtime_hours"
    assert output.fields[0].field_id != output.fields[1].field_id


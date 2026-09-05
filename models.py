from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional



class Evidence(BaseModel):
    page: int = Field(ge=1)
    bbox: list[float] = Field(min_length=4, max_length=4)
    text_snippet: str


class ExtractedField(BaseModel):
    field_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    value: str
    evidence: Evidence
    extraction_confidence: Literal["high", "medium", "low"]


class EstablishmentProfile(BaseModel):
    state: str
    sector: str
    headcount: Optional[int] = None
    contractor_involved: Optional[bool] = None
    worker_type: Optional[str] = None


class DocumentQuality(BaseModel):
    overall_score: float = Field(ge=0, le=1)
    issues: list[str] = Field(default_factory=list)


class ExtractionOutput(BaseModel):
    document_id: str
    establishment_profile: EstablishmentProfile
    document_quality: DocumentQuality
    fields: list[ExtractedField]

    @model_validator(mode="after")
    def validate_unique_field_names(self):
        names = [field.name for field in self.fields]
        if len(names) != len(set(names)):
            raise ValueError("field names must be unique")
        return self



class Citation(BaseModel):
    code: str
    section: str


class Finding(BaseModel):
    finding_id: str
    type: Literal["missing", "discrepancy", "substantive", "cannot_determine"]
    severity: Optional[int] = None
    related_field_id: Optional[str] = None
    citation: Optional[Citation] = None
    explanation: str
    confidence: Optional[Literal["high", "medium", "low"]] = None
    employer_action: Optional[str] = None
    inspector_action: Optional[str] = None
    human_review_required: bool = True
    reason: Optional[str] = None
    missing_context: list[str] = Field(default_factory=list)


class FindingsOutput(BaseModel):
    document_id: str
    risk_score: float
    risk_tier: Literal["low", "medium", "high"]
    findings: list[Finding]
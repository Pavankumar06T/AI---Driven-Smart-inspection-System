from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class EstablishmentProfile(BaseModel):
    """Profile details of the establishment under inspection."""
    state: str = Field(..., description="Indian State/UT (e.g. Maharashtra, Karnataka, Delhi)")
    sector: str = Field(..., description="Industry Sector (e.g. Factory, Construction, Mining, Service)")
    headcount: Optional[int] = Field(None, description="Total employee headcount")
    contractor_involved: Optional[bool] = Field(None, description="Whether contract labor is deployed")
    worker_type: Optional[str] = Field(None, description="Worker type (e.g., Unskilled, Skilled, Hazardous)")


class ProfileCreateRequest(BaseModel):
    """Payload to create or update an establishment profile for a document."""
    document_id: Optional[str] = Field(None, description="Optional document ID if already created")
    state: str
    sector: str
    headcount: Optional[int] = None
    contractor_involved: Optional[bool] = None
    worker_type: Optional[str] = None


class Evidence(BaseModel):
    """Bounding box and text snippet evidence for an extracted field."""
    page: int = Field(..., ge=1, description="1-indexed page number where the field was found")
    bbox: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Bounding box [x, y, w, h] normalized as percentages (0 to 100) relative to page dimensions"
    )
    text_snippet: str = Field(..., description="Raw text snippet extracted from the region")


class ExtractedField(BaseModel):
    """Individual extracted field record with grounded evidence and confidence."""
    field_id: str = Field(..., description="Unique field identifier within document, e.g. 'f1', 'f2'")
    name: str = Field(..., description="Canonical compliance field name")
    value: str = Field(..., description="Extracted value string")
    evidence: Evidence = Field(..., description="Visual evidence location and snippet")
    extraction_confidence: Literal["high", "medium", "low"] = Field(
        ..., description="Confidence rating: high (clear/legible), medium (minor uncertainty), low (blurred/ambiguous)"
    )


class DocumentQuality(BaseModel):
    """Evaluation of document legibility, completeness, and visual quality."""
    overall_score: float = Field(..., ge=0.0, le=1.0, description="Score from 0.0 (unusable) to 1.0 (perfect)")
    issues: List[str] = Field(default_factory=list, description="List of quality defects observed")


class ExtractionOutput(BaseModel):
    """Fixed JSON output contract consumed by downstream Compliance Reasoning Module."""
    document_id: str = Field(..., description="Unique document ID")
    establishment_profile: EstablishmentProfile = Field(..., description="Establishment metadata")
    document_quality: DocumentQuality = Field(..., description="Document quality evaluation")
    fields: List[ExtractedField] = Field(default_factory=list, description="List of extracted compliance fields with evidence")

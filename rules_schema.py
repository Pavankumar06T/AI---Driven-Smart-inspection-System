from pydantic import BaseModel
from typing import Literal, Optional


class ComplianceRule(BaseModel):
    check_id: str
    scenario: Literal[
        "wage_reconciliation",
        "safety_documentation",
        "registration_licensing"
    ]
    title: str
    code: str
    section: str
    clause_text: str
    condition: str
    applies_when: dict
    field_dependencies: list[str]
    severity: int
    violation_type: Literal["missing", "discrepancy", "substantive"]
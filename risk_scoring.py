"""
Aggregates findings into a severity-weighted risk score and tier,
and assembles the final FindingsOutput.
"""

from models import Finding, FindingsOutput

SEVERITY_WEIGHTS = {1: 2, 2: 4, 3: 8, 4: 15, 5: 25}

TIER_THRESHOLDS = [
    (0, "low"),
    (15, "medium"),
    (35, "high"),
]


def calculate_risk_score(findings: list[Finding]) -> tuple[float, str]:
    """Sum severity-weighted points across all actual violations.
    cannot_determine findings contribute 0 — they're not violations,
    they're honesty about missing data, and shouldn't be punished."""
    total = 0
    for f in findings:
        if f.type == "cannot_determine":
            continue
        weight = SEVERITY_WEIGHTS.get(f.severity, 0)
        total += weight

    tier = "low"
    for threshold, tier_name in TIER_THRESHOLDS:
        if total >= threshold:
            tier = tier_name

    return float(total), tier


def build_findings_output(document_id: str, findings: list[Finding]) -> FindingsOutput:
    risk_score, risk_tier = calculate_risk_score(findings)
    return FindingsOutput(
        document_id=document_id,
        risk_score=risk_score,
        risk_tier=risk_tier,
        findings=findings,
    )
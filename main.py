"""
FastAPI app exposing /analyze — the endpoint Person 1's real
/extract output (or your mock fixtures) gets sent to.
"""

from fastapi import FastAPI, HTTPException
import logging
from models import ExtractionOutput, FindingsOutput
from retrieval import retrieve_relevant_rules
from reasoning import generate_findings
from risk_scoring import build_findings_output

app = FastAPI(title="PS-05 Compliance Reasoning Module")
logger = logging.getLogger(__name__)


@app.post("/analyze", response_model=FindingsOutput)
def analyze(extraction: ExtractionOutput) -> FindingsOutput:
    try:
        rules = retrieve_relevant_rules(extraction)
        findings = generate_findings(extraction, rules)
        return build_findings_output(extraction.document_id, findings)
    except Exception as e:
        logger.exception("Analysis failed for document %s", extraction.document_id)
        raise HTTPException(status_code=500, detail="Analysis failed") from e


@app.get("/health")
def health():
    return {"status": "ok"}
from models import ExtractionOutput
from retrieval import retrieve_relevant_rules
from reasoning import generate_findings
from risk_scoring import build_findings_output

from test_reasoning_v2 import sample

extraction = ExtractionOutput(**sample)
rules = retrieve_relevant_rules(extraction)
findings = generate_findings(extraction, rules)
output = build_findings_output(extraction.document_id, findings)

print(f"Risk score: {output.risk_score}, Tier: {output.risk_tier}")
print(f"Total findings: {len(output.findings)}")
print(output.model_dump_json(indent=2))
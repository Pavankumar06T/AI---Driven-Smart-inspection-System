import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.models import ExtractionOutput

client = TestClient(app)

FIXTURES_DIR = Path(__file__).resolve().parent / "test_fixtures"

fixtures = [
    "wage_register_blurred.jpg",
    "safety_inspection_clean.pdf",
    "factory_license_scanned.pdf"
]

print("=" * 65)
print("VERIFYING /extract ENDPOINT ON ALL 3 TEST FIXTURES")
print("=" * 65)

for fixture_name in fixtures:
    file_path = FIXTURES_DIR / fixture_name
    assert file_path.exists(), f"Fixture missing: {file_path}"
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    mime_type = "application/pdf" if fixture_name.endswith(".pdf") else "image/jpeg"
    files = {"file": (fixture_name, file_bytes, mime_type)}
    data = {
        "state": "Maharashtra",
        "sector": "Factory",
        "headcount": "100"
    }

    res = client.post("/extract", files=files, data=data)
    print(f"\n[FIXTURE] {fixture_name}")
    print(f"   HTTP Status: {res.status_code}")
    assert res.status_code == 200, f"Failed: {res.text}"

    json_data = res.json()
    # Validate against Pydantic schema
    output_obj = ExtractionOutput(**json_data)
    
    fields = output_obj.fields
    quality = output_obj.document_quality
    
    print(f"   Extracted Fields Count: {len(fields)}")
    print(f"   Document Quality Score: {quality.overall_score * 100:.0f}%")
    print(f"   Quality Issues Logged: {quality.issues}")
    print("   Extracted Field Summary:")
    for f in fields:
        print(f"     - [{f.field_id}] {f.name}: '{f.value}' | Conf: {f.extraction_confidence} | BBox: {f.evidence.bbox}")


print("\n" + "=" * 65)
print("SUCCESS: ALL 3 FIXTURES EXTRACTED & SCHEMA VALIDATED 100%")
print("=" * 65)

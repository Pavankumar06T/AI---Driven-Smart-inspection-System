import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "Document Intelligence Module" in data["module"]

def test_post_profile():
    payload = {
        "state": "Maharashtra",
        "sector": "Factory",
        "headcount": 120,
        "contractor_involved": True,
        "worker_type": "Skilled"
    }
    response = client.post("/profile", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["establishment_profile"]["state"] == "Maharashtra"
    assert data["establishment_profile"]["headcount"] == 120

def test_post_extract_image():
    # Generate test image bytes
    buf = io.BytesIO()
    img = Image.new("RGB", (600, 800), color="white")
    img.save(buf, format="PNG")
    buf.seek(0)

    files = {"file": ("test_wage.png", buf, "image/png")}
    form_data = {
        "state": "Gujarat",
        "sector": "Chemical",
        "headcount": 50
    }

    response = client.post("/extract", files=files, data=form_data)
    assert response.status_code == 200
    result = response.json()

    assert "document_id" in result
    assert result["establishment_profile"]["state"] == "Gujarat"
    assert "document_quality" in result
    assert isinstance(result["fields"], list)
    
    doc_id = result["document_id"]

    # Verify GET /documents/{id}
    get_res = client.get(f"/documents/{doc_id}")
    assert get_res.status_code == 200
    assert get_res.json()["document_id"] == doc_id

    # Verify GET /documents/{id}/pages/1
    img_res = client.get(f"/documents/{doc_id}/pages/1")
    assert img_res.status_code == 200
    assert img_res.headers["content-type"] == "image/png"


def test_post_extract_pdf_clean():
    from pathlib import Path
    from app.models import ExtractionOutput

    fixtures_dir = Path(__file__).resolve().parent.parent / "test_fixtures"
    pdf_path = fixtures_dir / "safety_inspection_clean.pdf"
    assert pdf_path.exists(), "Clean PDF test fixture file missing."

    with open(pdf_path, "rb") as f:
        files = {"file": ("safety_inspection_clean.pdf", f.read(), "application/pdf")}
        data = {
            "state": "Maharashtra",
            "sector": "Chemical Manufacturing",
            "headcount": 45,
            "contractor_involved": "false",
            "worker_type": "Hazardous"
        }
        response = client.post("/extract", files=files, data=data)

    assert response.status_code == 200
    res = response.json()

    # Validate schema against ExtractionOutput Pydantic model
    output = ExtractionOutput(**res)
    assert output.establishment_profile.state == "Maharashtra"
    assert output.establishment_profile.sector == "Chemical Manufacturing"
    assert output.establishment_profile.headcount == 45
    assert len(output.fields) > 0

    for field in output.fields:
        assert field.field_id
        assert field.name
        assert field.value
        assert len(field.evidence.bbox) == 4
        assert field.evidence.text_snippet


def test_post_extract_pdf_scanned():
    from pathlib import Path
    from app.models import ExtractionOutput

    fixtures_dir = Path(__file__).resolve().parent.parent / "test_fixtures"
    pdf_path = fixtures_dir / "factory_license_scanned.pdf"
    assert pdf_path.exists(), "Scanned PDF test fixture file missing."

    with open(pdf_path, "rb") as f:
        files = {"file": ("factory_license_scanned.pdf", f.read(), "application/pdf")}
        data = {
            "state": "Maharashtra",
            "sector": "Automobile Factory",
            "headcount": 250,
            "contractor_involved": "true",
            "worker_type": "Skilled"
        }
        response = client.post("/extract", files=files, data=data)

    assert response.status_code == 200
    res = response.json()

    # Validate schema against ExtractionOutput Pydantic model
    output = ExtractionOutput(**res)
    assert output.establishment_profile.state == "Maharashtra"
    assert output.establishment_profile.sector == "Automobile Factory"
    assert output.establishment_profile.headcount == 250
    assert output.establishment_profile.contractor_involved is True
    assert len(output.fields) > 0

    for field in output.fields:
        assert field.field_id
        assert field.name
        assert field.value
        assert len(field.evidence.bbox) == 4
        assert field.evidence.text_snippet


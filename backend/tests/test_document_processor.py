import pytest
from pathlib import Path
from PIL import Image
from app.document_processor import save_uploaded_file, process_document_to_images

def test_save_uploaded_file(tmp_path, monkeypatch):
    monkeypatch.setattr("app.document_processor.UPLOADS_DIR", tmp_path)
    content = b"fake pdf contents"
    doc_id, target_path = save_uploaded_file(content, "test.pdf")
    
    assert doc_id.startswith("doc_")
    assert target_path.exists()
    assert target_path.read_bytes() == content

def test_process_image_document(tmp_path, monkeypatch):
    monkeypatch.setattr("app.document_processor.PAGES_DIR", tmp_path)
    
    # Create sample PNG image file
    sample_img_path = tmp_path / "sample.png"
    img = Image.new("RGB", (800, 600), color="white")
    img.save(sample_img_path, "PNG")

    pages = process_document_to_images(sample_img_path, "doc_test_img")
    assert len(pages) == 1
    assert pages[0].exists()
    assert pages[0].name == "doc_test_img_page_1.png"

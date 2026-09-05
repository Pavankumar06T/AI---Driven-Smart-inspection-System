import json
from typing import Optional
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Path as APIPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.database import init_db, save_profile, get_profile, save_extraction, get_extraction
from app.models import ProfileCreateRequest, EstablishmentProfile, ExtractionOutput
from app.document_processor import save_uploaded_file, process_document_to_images
from app.gemini_extractor import extract_with_gemini_vision
from app.config import PAGES_DIR

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="PS-05 Document Intelligence Module API",
    description="Vision-based labor compliance extraction and evidence grounding API for Digital Shram Sankalp Ideathon 2026",
    version="1.0.0",
    lifespan=lifespan
)

# Ensure DB is initialized immediately on import
init_db()

# Enable CORS for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "module": "Document Intelligence Module (PS-05 Prototype)",
        "event": "Digital Shram Sankalp Ideathon 2026",
        "ministry": "Ministry of Labour & Employment, India"
    }

@app.post("/profile")
def create_or_update_profile(payload: ProfileCreateRequest):
    """
    POST /profile — accepts state, sector, headcount, contractor_involved, worker_type.
    Stores establishment profile against document_id.
    """
    doc_id = payload.document_id or f"doc_{Path(save_uploaded_file(b'', 'temp.txt')[1]).stem}"
    save_profile(
        document_id=doc_id,
        state=payload.state,
        sector=payload.sector,
        headcount=payload.headcount,
        contractor_involved=payload.contractor_involved,
        worker_type=payload.worker_type
    )
    
    saved_profile = get_profile(doc_id)
    return {
        "message": "Establishment profile stored successfully",
        "document_id": doc_id,
        "establishment_profile": saved_profile
    }

@app.post("/extract", response_model=ExtractionOutput)
async def extract_document(
    file: UploadFile = File(...),
    document_id: Optional[str] = Form(None),
    state: Optional[str] = Form("Maharashtra"),
    sector: Optional[str] = Form("Factory"),
    headcount: Optional[int] = Form(None),
    contractor_involved: Optional[bool] = Form(None),
    worker_type: Optional[str] = Form(None)
):
    """
    POST /extract — accepts document upload (PDF, scanned PDF, JPG/PNG image),
    normalizes into page images, runs Gemini Vision API extraction, and returns ExtractionOutput JSON.
    """
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Save raw uploaded file
    new_doc_id, file_path = save_uploaded_file(contents, file.filename)
    doc_id = document_id or new_doc_id

    # Check if profile already exists in DB, or merge form inputs
    existing_profile = get_profile(doc_id)
    if not existing_profile:
        save_profile(
            document_id=doc_id,
            state=state or "Maharashtra",
            sector=sector or "Factory",
            headcount=headcount,
            contractor_involved=contractor_involved,
            worker_type=worker_type
        )
        profile_dict = get_profile(doc_id)
    else:
        profile_dict = existing_profile

    # Normalize PDF or Image into page images
    try:
        page_image_paths = process_document_to_images(file_path, doc_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Document normalization failed: {str(e)}")

    # Vision Extraction with Gemini API
    extraction_result = extract_with_gemini_vision(page_image_paths, doc_id, profile_dict, original_filename=file.filename)

    # Save to DB
    page_rel_paths = [img.name for img in page_image_paths]
    save_extraction(
        document_id=doc_id,
        original_filename=file.filename,
        file_path=str(file_path),
        num_pages=len(page_image_paths),
        page_image_paths=page_rel_paths,
        extraction_data=extraction_result.model_dump()
    )

    return extraction_result

@app.get("/fixtures/{filename}")
def get_test_fixture_file(filename: str):
    """Serves sample test fixture files (JPG / PDF) for live hackathon demonstration."""
    fixture_dir = Path(__file__).resolve().parent.parent / "test_fixtures"
    fixture_path = fixture_dir / filename
    if not fixture_path.exists():
        raise HTTPException(status_code=404, detail=f"Fixture file '{filename}' not found.")
    media_type = "application/pdf" if filename.endswith(".pdf") else "image/jpeg"
    return FileResponse(fixture_path, media_type=media_type)

@app.get("/documents/{document_id}", response_model=ExtractionOutput)
def get_document_extraction(document_id: str = APIPath(..., description="Document ID")):
    """Retrieves ExtractionOutput JSON for a document."""
    record = get_extraction(document_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Document ID '{document_id}' not found.")
    return record["extraction_data"]

@app.get("/documents/{document_id}/pages/{page_num}")
def get_document_page_image(
    document_id: str = APIPath(...),
    page_num: int = APIPath(..., ge=1)
):
    """Serves the rendered page PNG image for evidence-overlay canvas rendering."""
    record = get_extraction(document_id)
    if not record:
        # Fallback check directly in storage pages
        target_file = PAGES_DIR / f"{document_id}_page_{page_num}.png"
        if target_file.exists():
            return FileResponse(target_file, media_type="image/png")
        raise HTTPException(status_code=404, detail="Document not found")

    page_files = record["page_image_paths"]
    if page_num > len(page_files):
        raise HTTPException(status_code=404, detail=f"Page {page_num} does not exist for document.")

    image_filename = page_files[page_num - 1]
    image_path = PAGES_DIR / image_filename
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Page image file missing: {image_filename}")

    return FileResponse(image_path, media_type="image/png")


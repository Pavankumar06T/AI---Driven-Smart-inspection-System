import os
import uuid
from typing import List, Tuple
from pathlib import Path
from PIL import Image, ImageOps
from app.config import PAGES_DIR, UPLOADS_DIR

def save_uploaded_file(file_bytes: bytes, filename: str) -> Tuple[str, Path]:
    """Saves raw uploaded file bytes to UPLOADS_DIR and returns document_id and saved path."""
    ext = Path(filename).suffix.lower()
    doc_id = f"doc_{uuid.uuid4().hex[:10]}"
    target_path = UPLOADS_DIR / f"{doc_id}{ext}"
    
    with open(target_path, "wb") as f:
        f.write(file_bytes)
        
    return doc_id, target_path

def process_document_to_images(file_path: Path, doc_id: str) -> List[Path]:
    """
    Normalizes clean PDFs, scanned PDFs, and image files (JPG, PNG, WEBP)
    into a list of standardized PNG page image files saved in PAGES_DIR.
    """
    ext = file_path.suffix.lower()
    page_image_paths = []

    if ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"]:
        # Single image upload
        img = Image.open(file_path)
        img = ImageOps.exif_transpose(img) # Correct orientation if EXIF present
        if img.mode != "RGB":
            img = img.convert("RGB")
            
        page_filename = f"{doc_id}_page_1.png"
        save_path = PAGES_DIR / page_filename
        img.save(save_path, "PNG")
        page_image_paths.append(save_path)

    elif ext == ".pdf":
        images = []
        # Attempt 1: pdf2image
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(file_path, dpi=200)
        except Exception as e:
            # Attempt 2: PyMuPDF (fitz) fallback if poppler is not installed on Windows
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(file_path)
                for page in doc:
                    pix = page.get_pixmap(dpi=200)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    images.append(img)
                doc.close()
            except Exception as e2:
                raise RuntimeError(
                    f"Failed to convert PDF to image. Tried pdf2image ({e}) and PyMuPDF ({e2}). "
                    "Please ensure poppler or pymupdf is installed."
                )

        if not images:
            raise ValueError("PDF contained 0 pages or could not be rendered.")

        for idx, img in enumerate(images, start=1):
            if img.mode != "RGB":
                img = img.convert("RGB")
            page_filename = f"{doc_id}_page_{idx}.png"
            save_path = PAGES_DIR / page_filename
            img.save(save_path, "PNG")
            page_image_paths.append(save_path)

    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return page_image_paths

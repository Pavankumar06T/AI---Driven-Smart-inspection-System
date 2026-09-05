import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = os.getenv("STORAGE_DIR", str(BASE_DIR / "storage"))
PAGES_DIR = Path(STORAGE_DIR) / "pages"
UPLOADS_DIR = Path(STORAGE_DIR) / "uploads"
DB_PATH = Path(STORAGE_DIR) / "app.db"

# Ensure directories exist
PAGES_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Gemini API configuration
# Note: Google's current stable multimodal vision models as of 2025/2026: gemini-2.5-flash / gemini-1.5-flash
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Host / Port settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

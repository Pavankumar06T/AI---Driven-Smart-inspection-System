import sqlite3
import json
from typing import Optional, Dict, Any
from app.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS establishment_profiles (
        document_id TEXT PRIMARY KEY,
        state TEXT NOT NULL,
        sector TEXT NOT NULL,
        headcount INTEGER,
        contractor_involved INTEGER,
        worker_type TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_extractions (
        document_id TEXT PRIMARY KEY,
        original_filename TEXT NOT NULL,
        file_path TEXT NOT NULL,
        num_pages INTEGER DEFAULT 1,
        page_image_paths TEXT NOT NULL, -- JSON array of page image paths
        extraction_data TEXT NOT NULL,  -- JSON string of ExtractionOutput
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_profile(document_id: str, state: str, sector: str, headcount: Optional[int] = None,
                 contractor_involved: Optional[bool] = None, worker_type: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO establishment_profiles (document_id, state, sector, headcount, contractor_involved, worker_type, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(document_id) DO UPDATE SET
        state=excluded.state,
        sector=excluded.sector,
        headcount=excluded.headcount,
        contractor_involved=excluded.contractor_involved,
        worker_type=excluded.worker_type,
        updated_at=CURRENT_TIMESTAMP
    """, (
        document_id,
        state,
        sector,
        headcount,
        1 if contractor_involved is True else (0 if contractor_involved is False else None),
        worker_type
    ))
    conn.commit()
    conn.close()

def get_profile(document_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM establishment_profiles WHERE document_id = ?", (document_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "state": row["state"],
        "sector": row["sector"],
        "headcount": row["headcount"],
        "contractor_involved": bool(row["contractor_involved"]) if row["contractor_involved"] is not None else None,
        "worker_type": row["worker_type"]
    }

def save_extraction(document_id: str, original_filename: str, file_path: str,
                    num_pages: int, page_image_paths: list, extraction_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO document_extractions (document_id, original_filename, file_path, num_pages, page_image_paths, extraction_data, created_at)
    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(document_id) DO UPDATE SET
        original_filename=excluded.original_filename,
        file_path=excluded.file_path,
        num_pages=excluded.num_pages,
        page_image_paths=excluded.page_image_paths,
        extraction_data=excluded.extraction_data,
        created_at=CURRENT_TIMESTAMP
    """, (
        document_id,
        original_filename,
        file_path,
        num_pages,
        json.dumps(page_image_paths),
        json.dumps(extraction_data)
    ))
    conn.commit()
    conn.close()

def get_extraction(document_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM document_extractions WHERE document_id = ?", (document_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "document_id": row["document_id"],
        "original_filename": row["original_filename"],
        "file_path": row["file_path"],
        "num_pages": row["num_pages"],
        "page_image_paths": json.loads(row["page_image_paths"]),
        "extraction_data": json.loads(row["extraction_data"]),
        "created_at": row["created_at"]
    }

import uuid

from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent 
DOCUMENTS_DIR = BASE_DIR / "media" / "documents"

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".txt"}


def process_document(obj_type: str, content: bytes, original_filename: str) -> str:
    ext = Path(original_filename).suffix.lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Недопустимый формат файла: {ext}")
    
    filename = f"{uuid.uuid4().hex}{ext}"
    
    target_dir = DOCUMENTS_DIR / obj_type
    target_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = target_dir / filename
    filepath.write_bytes(content)

    return f"{obj_type}/{filename}"


def delete_document(obj_type: str, filename: str | None) -> None:
    if filename is None:
        return

    filepath = DOCUMENTS_DIR / obj_type / filename
    if filepath.exists():
        filepath.unlink()
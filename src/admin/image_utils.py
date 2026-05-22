import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent.parent 
PROFILE_PICS_DIR = BASE_DIR / "media" / "pictures"
DOCS_FILES_DIR = BASE_DIR / "media" / "docs"


def process_image(obj_type: str, content: bytes, crop: bool = True) -> str:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)
        
        if crop:
            min_side = min(img.size) 
            img = ImageOps.fit(img, (min_side, min_side), method=Image.Resampling.LANCZOS)
        
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"
        
        target_dir = PROFILE_PICS_DIR / obj_type
        target_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = target_dir / filename
        
        img.save(filepath, "JPEG", quality=95, optimize=False)
        

    return filename


def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return

    filepath = PROFILE_PICS_DIR / filename
    print(f"FILEPATH: {filepath}")
    if filepath.exists():
        filepath.unlink()
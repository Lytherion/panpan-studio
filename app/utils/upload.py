import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from PIL import Image
from app.config import settings

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi"}

def ensure_upload_dir(subdir: str = ""):
    upload_path = Path(settings.UPLOAD_DIR) / subdir
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path

async def save_upload_file(file: UploadFile, subdir: str = "") -> str:
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件过大")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS and file_ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    upload_dir = ensure_upload_dir(subdir)
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = upload_dir / file_name

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # 图片压缩
    if file_ext in ALLOWED_IMAGE_EXTENSIONS:
        try:
            img = Image.open(file_path)
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")
            img.save(file_path, optimize=True, quality=85)
        except Exception:
            pass

    return f"{subdir}/{file_name}" if subdir else file_name

def delete_upload_file(file_path: str):
    full_path = Path(settings.UPLOAD_DIR) / file_path
    if full_path.exists():
        full_path.unlink()

import os
import uuid
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import BadRequestException
from app.core.logging import logger

async def save_uploaded_file(file: UploadFile, folder: str) -> str:
    filename = file.filename or "file"
    ext = filename.split(".")[-1].lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise BadRequestException(message=f"File extension '.{ext}' is not allowed")
        
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise BadRequestException(message="File size exceeds limit")
    await file.seek(0)
    
    target_dir = os.path.join(settings.UPLOAD_DIR, folder)
    os.makedirs(target_dir, exist_ok=True)
    
    unique_filename = f"{uuid.uuid4()}.{ext}"
    dest_path = os.path.join(target_dir, unique_filename)
    
    with open(dest_path, "wb") as f:
        f.write(content)
        
    return f"static/uploads/{folder}/{unique_filename}"

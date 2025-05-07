import os
import hashlib
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings

async def save_upload_file(upload_file: UploadFile, destination: Optional[str] = None) -> str:
    """Save an uploaded file to the specified destination."""
    if destination is None:
        destination = settings.UPLOAD_DIR
    
    # Create a unique filename
    file_extension = os.path.splitext(upload_file.filename)[1]
    file_hash = hashlib.md5(upload_file.filename.encode()).hexdigest()
    filename = f"{file_hash}{file_extension}"
    
    # Ensure the destination directory exists
    os.makedirs(destination, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(destination, filename)
    with open(file_path, "wb") as f:
        content = await upload_file.read()
        f.write(content)
    
    return file_path

def validate_file_type(file: UploadFile, allowed_types: list) -> bool:
    """Validate if the uploaded file type is allowed."""
    return file.content_type in allowed_types

def get_file_size(file_path: str) -> int:
    """Get the size of a file in bytes."""
    return os.path.getsize(file_path)

def format_file_size(size_in_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB" 
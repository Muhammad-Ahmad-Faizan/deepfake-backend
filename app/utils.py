import os
import shutil
from pathlib import Path
from datetime import datetime
from app.config import settings

def create_upload_directory():
    """Create upload directory if it doesn't exist"""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

def save_upload_file(file, filename: str) -> str:
    """Save uploaded file to disk"""
    upload_dir = create_upload_directory()
    
    # Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(filename)
    unique_filename = f"{timestamp}_{name}{ext}"
    
    file_path = upload_dir / unique_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return str(file_path)

def delete_file(file_path: str):
    """Delete file from disk"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    return os.path.getsize(file_path)

def validate_file_type(filename: str) -> str:
    """Validate and return file type"""
    ext = os.path.splitext(filename)[1].lower()
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    audio_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a']
    
    if ext in video_extensions:
        return "video"
    elif ext in audio_extensions:
        return "audio"
    else:
        raise ValueError(f"Unsupported file type: {ext}")

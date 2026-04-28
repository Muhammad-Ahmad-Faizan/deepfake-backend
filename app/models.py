from datetime import datetime
from enum import Enum
from typing import Optional, List
from bson import ObjectId
import base64
import io

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class PredictionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# User Document Model
class User:
    def __init__(self, email: str, username: str, hashed_password: str, 
                 role: UserRole = UserRole.USER, is_active: bool = True):
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.role = role.value if isinstance(role, UserRole) else role
        self.is_active = is_active
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at
        }

# Video Document Model
class Video:
    def __init__(self, user_id: str, filename: str, original_filename: str,
                 file_path: str, file_size: int, file_type: str = "video"):
        self.user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        self.filename = filename
        self.original_filename = original_filename
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type
        self.status = PredictionStatus.PENDING.value
        self.is_deepfake = None
        self.confidence_score = None
        self.prediction_details = None
        self.uploaded_at = datetime.utcnow()
        self.processed_at = None
        self.thumbnail_base64 = None  # Base64 encoded thumbnail
        self.annotated_frames_base64 = []  # List of base64 encoded frames
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "file_type": self.file_type,
            "status": self.status,
            "is_deepfake": self.is_deepfake,
            "confidence_score": self.confidence_score,
            "prediction_details": self.prediction_details,
            "uploaded_at": self.uploaded_at,
            "processed_at": self.processed_at,
            "thumbnail_base64": self.thumbnail_base64,
            "annotated_frames_base64": self.annotated_frames_base64
        }

# Helper functions for Base64 encoding
def encode_image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to Base64 string"""
    return base64.b64encode(image_bytes).decode('utf-8')

def decode_base64_to_image(base64_string: str) -> bytes:
    """Convert Base64 string back to image bytes"""
    return base64.b64decode(base64_string.encode('utf-8'))

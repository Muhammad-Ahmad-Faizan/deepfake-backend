from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from datetime import datetime
import os

from app.database import get_db
from app.models import User, Video, PredictionStatus
from app.schemas import VideoResponse
from app.auth import get_current_user
from app.utils import save_upload_file, get_file_size, validate_file_type
from app.config import settings

router = APIRouter()

@router.post("/video", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def upload_video(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """Upload a video file for deepfake detection"""
    
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    # Validate file type
    try:
        file_type = validate_file_type(file.filename)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Check file size (read first to get size)
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Reset file pointer and save
    await file.seek(0)
    file_path = save_upload_file(file, file.filename)
    
    # Create database record
    new_video = Video(
        filename=os.path.basename(file_path),
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file_type,
        status=PredictionStatus.PENDING,
        user_id=str(current_user.get("_id")) if "_id" in current_user else current_user.get("id")
    )
    
    result = db.videos.insert_one(new_video.to_dict())
    
    return {"id": str(result.inserted_id), "filename": new_video.filename, "status": new_video.status}

@router.get("/videos", response_model=list[VideoResponse])
async def get_user_videos(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """Get all videos uploaded by current user"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    user_id = str(current_user.get("_id")) if "_id" in current_user else current_user.get("id")
    videos = list(db.videos.find({"user_id": user_id}).skip(skip).limit(limit))
    return videos

@router.get("/videos/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: str,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """Get specific video by ID"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    from bson import ObjectId
    try:
        video_oid = ObjectId(video_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid video ID"
        )
    
    video = db.videos.find_one({"_id": video_oid})
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    return video

@router.delete("/videos/{video_id}")
async def delete_video(
    video_id: str,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """Delete a video"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    from bson import ObjectId
    try:
        video_oid = ObjectId(video_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid video ID"
        )
    
    video = db.videos.find_one({"_id": video_oid})
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    # Delete from database
    db.videos.delete_one({"_id": video_oid})
    
    return {"message": "Video deleted successfully"}

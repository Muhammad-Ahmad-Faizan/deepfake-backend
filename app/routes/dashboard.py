from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import User, Video, PredictionStatus
from app.schemas import DashboardStats, VideoResponse
from app.auth import get_current_user

router = APIRouter()

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user dashboard statistics"""
    
    # Total videos uploaded by user
    total_videos = db.query(func.count(Video.id)).filter(
        Video.user_id == current_user.id
    ).scalar()
    
    # Videos analyzed (completed)
    videos_analyzed = db.query(func.count(Video.id)).filter(
        Video.user_id == current_user.id,
        Video.status == PredictionStatus.COMPLETED
    ).scalar()
    
    # Deepfakes detected
    deepfakes_detected = db.query(func.count(Video.id)).filter(
        Video.user_id == current_user.id,
        Video.is_deepfake == True
    ).scalar()
    
    # Recent uploads (last 5)
    recent_uploads = db.query(Video).filter(
        Video.user_id == current_user.id
    ).order_by(Video.uploaded_at.desc()).limit(5).all()
    
    return {
        "total_videos": total_videos,
        "videos_analyzed": videos_analyzed,
        "deepfakes_detected": deepfakes_detected,
        "recent_uploads": recent_uploads
    }

@router.get("/recent-activity", response_model=list[VideoResponse])
async def get_recent_activity(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get user's recent video activity"""
    recent_videos = db.query(Video).filter(
        Video.user_id == current_user.id
    ).order_by(Video.uploaded_at.desc()).limit(limit).all()
    
    return recent_videos

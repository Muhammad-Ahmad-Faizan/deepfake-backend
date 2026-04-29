from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

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
    ).scalar() or 0
    
    # Videos analyzed (completed)
    total_predictions = db.query(func.count(Video.id)).filter(
        Video.user_id == current_user.id,
        Video.status == PredictionStatus.COMPLETED.value
    ).scalar() or 0
    
    # Deepfakes detected
    deepfakes_found = db.query(func.count(Video.id)).filter(
        Video.user_id == current_user.id,
        Video.is_deepfake == True
    ).scalar() or 0
    
    # Genuine videos (total analyzed - deepfakes)
    genuine_videos = total_predictions - deepfakes_found
    
    # Pending analyses (not yet completed)
    pending_analyses = db.query(func.count(Video.id)).filter(
        Video.user_id == current_user.id,
        Video.status.in_([PredictionStatus.PENDING.value, PredictionStatus.PROCESSING.value])
    ).scalar() or 0
    
    # Recent uploads (last 5)
    recent_uploads = db.query(Video).filter(
        Video.user_id == current_user.id
    ).order_by(Video.uploaded_at.desc()).limit(5).all()
    
    # Calculate success rate
    success_rate = (total_predictions / total_videos * 100) if total_videos > 0 else 0.0
    
    return {
        "total_videos": total_videos,
        "total_predictions": total_predictions,
        "deepfakes_found": deepfakes_found,
        "genuine_videos": genuine_videos,
        "pending_analyses": pending_analyses,
        "success_rate": success_rate
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

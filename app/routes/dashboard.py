from fastapi import APIRouter, Depends

from app.database import get_db
from app.models import User, Video, PredictionStatus
from app.schemas import DashboardStats, VideoResponse
from app.auth import get_current_user

router = APIRouter()

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """Get user dashboard statistics"""
    if db is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    user_id = str(current_user.get("_id")) if "_id" in current_user else current_user.get("id")
    
    # Total videos uploaded by user
    total_videos = db.videos.count_documents({"user_id": user_id})
    
    # Videos analyzed (completed)
    total_predictions = db.videos.count_documents({
        "user_id": user_id,
        "status": PredictionStatus.COMPLETED
    })
    
    # Deepfakes detected
    deepfakes_found = db.videos.count_documents({
        "user_id": user_id,
        "is_deepfake": True
    })
    
    # Genuine videos (total analyzed - deepfakes)
    genuine_videos = total_predictions - deepfakes_found
    
    # Pending analyses (not yet completed)
    pending_analyses = db.videos.count_documents({
        "user_id": user_id,
        "status": {"$in": [PredictionStatus.PENDING, PredictionStatus.PROCESSING]}
    })
    
    # Recent uploads (last 5)
    recent_uploads = list(db.videos.find(
        {"user_id": user_id}
    ).sort("uploaded_at", -1).limit(5))
    
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
    db=Depends(get_db),
    limit: int = 10
):
    """Get user's recent video activity"""
    if db is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    user_id = str(current_user.get("_id")) if "_id" in current_user else current_user.get("id")
    recent_videos = list(db.videos.find(
        {"user_id": user_id}
    ).sort("uploaded_at", -1).limit(limit))
    
    return recent_videos

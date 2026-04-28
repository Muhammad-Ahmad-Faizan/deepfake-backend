from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models import User, Video, UserRole
from app.schemas import AdminStats, UserResponse, AdminUserUpdate, VideoResponse
from app.auth import get_current_admin

router = APIRouter()

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Get admin dashboard statistics"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    # Total users
    total_users = db.users.count_documents({})
    
    # Total videos
    total_videos = db.videos.count_documents({})
    
    # Total deepfakes detected
    total_deepfakes = db.videos.count_documents({"is_deepfake": True})
    
    # Active users
    active_users = db.users.count_documents({"is_active": True})
    
    # Recent users (last 5)
    recent_users = list(db.users.find({}).sort("created_at", -1).limit(5))
    
    return {
        "total_users": total_users,
        "total_videos": total_videos,
        "total_deepfakes": total_deepfakes,
        "active_users": active_users,
        "recent_users": recent_users
    }

@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    current_admin: User = Depends(get_current_admin),
    db=Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all users (admin only)"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    users = list(db.users.find({}).skip(skip).limit(limit))
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_details(
    user_id: str,
    current_admin: User = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Get specific user details"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    from bson import ObjectId
    try:
        user_oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    user = db.users.find_one({"_id": user_oid})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: AdminUserUpdate,
    current_admin: User = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Update user (activate/deactivate, change role)"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    from bson import ObjectId
    try:
        user_oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    user = db.users.find_one({"_id": user_oid})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    update_data = {}
    if user_update.is_active is not None:
        update_data["is_active"] = user_update.is_active
    
    if user_update.role is not None:
        update_data["role"] = user_update.role
    
    if update_data:
        db.users.update_one({"_id": user_oid}, {"$set": update_data})
    
    updated_user = db.users.find_one({"_id": user_oid})
    return updated_user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_admin: User = Depends(get_current_admin),
    db=Depends(get_db)
):
    """Delete a user (admin only)"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    from bson import ObjectId
    try:
        user_oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    user = db.users.find_one({"_id": user_oid})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    current_admin_id = str(current_admin.get("_id")) if "_id" in current_admin else current_admin.get("id")
    if str(user_oid) == current_admin_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.users.delete_one({"_id": user_oid})
    
    return {"message": "User deleted successfully"}

@router.get("/videos", response_model=list[VideoResponse])
async def get_all_videos(
    current_admin: User = Depends(get_current_admin),
    db=Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all videos from all users (admin only)"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    videos = list(db.videos.find({}).sort(
        "uploaded_at", -1
    ).skip(skip).limit(limit))
    
    return videos

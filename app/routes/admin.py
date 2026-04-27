from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import User, Video, UserRole
from app.schemas import AdminStats, UserResponse, AdminUserUpdate, VideoResponse
from app.auth import get_current_admin

router = APIRouter()

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    
    # Total users
    total_users = db.query(func.count(User.id)).scalar()
    
    # Total videos
    total_videos = db.query(func.count(Video.id)).scalar()
    
    # Total deepfakes detected
    total_deepfakes = db.query(func.count(Video.id)).filter(
        Video.is_deepfake == True
    ).scalar()
    
    # Active users
    active_users = db.query(func.count(User.id)).filter(
        User.is_active == True
    ).scalar()
    
    # Recent users (last 5)
    recent_users = db.query(User).order_by(
        User.created_at.desc()
    ).limit(5).all()
    
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
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_details(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get specific user details"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: AdminUserUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update user (activate/deactivate, change role)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    
    if user_update.role is not None:
        user.role = user_update.role
    
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

@router.get("/videos", response_model=list[VideoResponse])
async def get_all_videos(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all videos from all users (admin only)"""
    videos = db.query(Video).order_by(
        Video.uploaded_at.desc()
    ).offset(skip).limit(limit).all()
    
    return videos

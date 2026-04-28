from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta

from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from app.config import settings

router = APIRouter()

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db=Depends(get_db)):
    """Register a new user"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    # Check if user already exists
    existing_user = db.users.find_one({"email": user_data.email})
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Generate username from email (before @)
    username = user_data.email.split('@')[0]
    
    # Check if username is taken, make it unique if needed
    base_username = username
    counter = 1
    while db.users.find_one({"username": username}):
        username = f"{base_username}{counter}"
        counter += 1
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=username,
        hashed_password=hashed_password,
        role=UserRole.USER
    )
    
    result = db.users.insert_one(new_user.to_dict())
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"email": user_data.email, "username": username}
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db=Depends(get_db)):
    """Login user and return JWT token"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    # Find user by email or username
    user = db.users.find_one({
        "$or": [
            {"email": credentials.username},
            {"username": credentials.username}
        ]
    })
    
    if not user or not verify_password(credentials.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"email": user["email"], "username": user.get("username")}
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(email=current_user.get("email"), username=current_user.get("username"))

@router.post("/logout")
async def logout(current_user=Depends(get_current_user)):
    """Logout user (client should delete token)"""
    return {"message": "Successfully logged out"}

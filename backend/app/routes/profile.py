"""
MedGuard — Profile Router
POST /api/profile  →  Create/Update a profile
GET /api/profiles/{id} → Get profile data
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Profile
from app.schemas import ProfileCreate, ProfileResponse

router = APIRouter(prefix="/api", tags=["Profile"])


@router.get("/profiles/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/profile", response_model=ProfileResponse)
def create_or_update_profile(data: ProfileCreate, db: Session = Depends(get_db)):
    # Check if exists
    profile = db.query(Profile).filter(Profile.id == data.id).first()
    
    if profile:
        # Update existing
        if data.age is not None: profile.age = data.age
        if data.full_name is not None: profile.full_name = data.full_name
        if data.gender is not None: profile.gender = data.gender
        # Recalculate senior status if age changed
        if data.age is not None:
             profile.is_senior = data.age >= 60
    else:
        # Create new
        profile = Profile(
            id=data.id,
            full_name=data.full_name,
            age=data.age or 0,
            gender=data.gender,
            is_senior=(data.age or 0) >= 60,
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return profile

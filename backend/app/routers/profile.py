from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.schemas.profile import ProfileUpdate, ProfileOut
from app.auth.deps import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.get("", response_model=ProfileOut)
@router.get("/me", response_model=ProfileOut)
def get_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("", response_model=ProfileOut)
@router.put("/me", response_model=ProfileOut)
def update_user_profile(profile_in: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(profile, field):
            setattr(profile, field, value)

    profile.profile_completed = True

    db.commit()
    db.refresh(profile)
    return profile

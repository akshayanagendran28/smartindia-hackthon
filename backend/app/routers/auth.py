from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.schemas.auth import UserRegister, UserLogin, Token, UserOut
from app.auth.security import verify_password, get_password_hash, create_access_token
from app.auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )
    
    user = User(
        email=user_in.email.lower(),
        mobile=user_in.mobile,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role or "entrepreneur",
        state=user_in.state,
        district=user_in.district,
        preferred_language=user_in.preferred_language or "en"
    )
    db.add(user)
    db.flush()

    # Create empty initial profile
    profile = UserProfile(
        user_id=user.id,
        location_state=user_in.state,
        location_district=user_in.district,
        profile_completed=False
    )
    db.add(profile)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email.lower()).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is disabled.")

    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

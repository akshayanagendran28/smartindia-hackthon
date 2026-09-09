from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import jwt
from sqlalchemy.orm import Session
from app.config import settings
from app.database.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except Exception:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account")
    return user

def get_current_user_optional(db: Session = Depends(get_db), token: Optional[str] = Depends(oauth2_scheme_optional)) -> Optional[User]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            return None
        user_id = int(user_id_str)
        user = db.query(User).filter(User.id == user_id).first()
        return user if user and user.is_active else None
    except Exception:
        return None

def get_current_user_flexible(db: Session = Depends(get_db), token: Optional[str] = Depends(oauth2_scheme_optional)) -> User:
    """
    Returns authenticated user if valid token provided;
    Otherwise falls back to default active entrepreneur demo user for frictionless SIH demo testing.
    """
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id_str: str = payload.get("sub")
            if user_id_str:
                user = db.query(User).filter(User.id == int(user_id_str)).first()
                if user and user.is_active:
                    return user
        except Exception:
            pass

    # Fallback to demo entrepreneur user
    demo_user = db.query(User).filter(User.email == "rajesh.kumar@example.com").first()
    if not demo_user:
        demo_user = db.query(User).filter(User.role == "entrepreneur").first()
    if not demo_user:
        demo_user = db.query(User).first()
    return demo_user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ["admin", "supervisor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required"
        )
    return current_user

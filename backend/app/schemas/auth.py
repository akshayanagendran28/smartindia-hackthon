from pydantic import BaseModel
from typing import Optional
import datetime

class UserRegister(BaseModel):
    full_name: str
    email: str
    mobile: Optional[str] = None
    password: str
    state: Optional[str] = None
    district: Optional[str] = None
    preferred_language: Optional[str] = "en"
    role: Optional[str] = "entrepreneur"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"

class UserOut(BaseModel):
    id: int
    email: str
    mobile: Optional[str] = None
    full_name: str
    role: str
    state: Optional[str] = None
    district: Optional[str] = None
    preferred_language: str
    is_active: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

Token.model_rebuild()

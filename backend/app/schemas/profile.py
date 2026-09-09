from pydantic import BaseModel
from typing import Optional
import datetime

class ProfileBase(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    category: Optional[str] = "General"
    annual_family_income: Optional[float] = 0.0
    existing_loans: Optional[float] = 0.0
    is_new_business: Optional[bool] = True
    business_type: Optional[str] = "Micro Retail"
    gstin: Optional[str] = None
    project_cost: Optional[float] = 0.0
    required_loan_amount: Optional[float] = 0.0
    purpose: Optional[str] = "Start a Business"
    is_student: Optional[bool] = False
    course: Optional[str] = None
    institution: Optional[str] = None
    education_cost: Optional[float] = 0.0
    location_state: Optional[str] = None
    location_district: Optional[str] = None
    pincode: Optional[str] = None
    profile_completed: Optional[bool] = False

class ProfileUpdate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

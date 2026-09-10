from pydantic import BaseModel
from typing import Optional
import datetime

class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    category: Optional[str] = "SC"
    social_category: Optional[str] = "SC"
    religion: Optional[str] = "hindu"
    is_differently_abled: Optional[bool] = False
    annual_family_income: Optional[float] = 0.0
    annual_income: Optional[float] = 0.0
    existing_loans: Optional[float] = 0.0
    own_contribution: Optional[float] = 0.0
    is_new_business: Optional[bool] = True
    business_stage: Optional[str] = "new"
    business_type: Optional[str] = "manufacturing"
    industry_sector: Optional[str] = None
    gstin: Optional[str] = None
    has_gst: Optional[bool] = False
    has_udyam_registration: Optional[bool] = False
    is_artisan: Optional[bool] = False
    is_street_vendor: Optional[bool] = False
    has_skill_training: Optional[bool] = False
    skill_training_details: Optional[str] = None
    project_cost: Optional[float] = 0.0
    required_loan_amount: Optional[float] = 0.0
    required_loan: Optional[float] = 0.0
    purpose: Optional[str] = "Start a Business"
    is_student: Optional[bool] = False
    education_qualification: Optional[str] = "graduate"
    course: Optional[str] = None
    institution: Optional[str] = None
    education_cost: Optional[float] = 0.0
    state: Optional[str] = None
    district: Optional[str] = None
    location_state: Optional[str] = None
    location_district: Optional[str] = None
    area_type: Optional[str] = "rural"
    pincode: Optional[str] = None
    profile_completed: Optional[bool] = False
    is_confirmed: Optional[bool] = False

class ProfileUpdate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

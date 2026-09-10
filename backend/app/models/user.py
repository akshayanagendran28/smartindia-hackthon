import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    mobile = Column(String(20), nullable=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="entrepreneur") # entrepreneur, student, admin, supervisor
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    preferred_language = Column(String(20), default="en") # en, hi, ta, te, kn, ml
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    documents = relationship("UserDocument", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    saved_schemes = relationship("SavedScheme", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Personal & Demographics
    full_name = Column(String(255), nullable=True)
    age = Column(Integer, default=28)
    gender = Column(String(30), default="female") # male, female, transgender
    category = Column(String(50), default="SC") # SC, ST, OBC, Minority, General
    social_category = Column(String(50), default="SC")
    religion = Column(String(50), default="hindu")
    is_differently_abled = Column(Boolean, default=False)
    
    # Financial
    annual_family_income = Column(Float, default=180000.0)
    annual_income = Column(Float, default=180000.0)
    existing_loans = Column(Float, default=0.0)
    credit_score_range = Column(String(50), default="700_750")
    has_existing_bank_account = Column(Boolean, default=True)
    has_collateral = Column(Boolean, default=False)
    own_contribution = Column(Float, default=150000.0)
    
    # Business & Project
    purpose_type = Column(String(50), default="BUSINESS") # BUSINESS, EDUCATION, SELF_EMPLOYMENT
    is_new_business = Column(Boolean, default=True)
    business_stage = Column(String(50), default="new") # new, expansion
    business_type = Column(String(100), default="manufacturing") # manufacturing, service, trading, street_vendor, artisan
    industry_sector = Column(String(100), default="food_processing")
    gstin = Column(String(50), nullable=True)
    has_gst = Column(Boolean, default=False)
    has_udyam_registration = Column(Boolean, default=True)
    is_artisan = Column(Boolean, default=False)
    is_street_vendor = Column(Boolean, default=False)
    project_cost = Column(Float, default=1500000.0)
    required_loan_amount = Column(Float, default=1200000.0)
    required_loan = Column(Float, default=1200000.0)
    purpose = Column(String(100), default="Start a Business")
    existing_turnover = Column(Float, default=0.0)
    
    # Education & Academic Details
    is_student = Column(Boolean, default=False)
    education_qualification = Column(String(50), default="graduate")
    current_education_level = Column(String(50), default="12th")
    course = Column(String(200), nullable=True)
    course_type = Column(String(100), default="Engineering / Technology")
    institution = Column(String(200), nullable=True)
    institution_type = Column(String(100), default="State Govt University")
    admission_status = Column(String(50), default="Confirmed / Admitted")
    annual_course_fee = Column(Float, default=150000.0)
    course_duration_years = Column(Integer, default=4)
    education_cost = Column(Float, default=0.0)
    has_training = Column(Boolean, default=True)
    has_skill_training = Column(Boolean, default=True)
    skill_training_details = Column(String(255), default="EDP 2-week certified")
    
    # Location
    location_state = Column(String(100), default="Maharashtra")
    location_district = Column(String(100), default="Mumbai")
    state = Column(String(100), default="Maharashtra")
    district = Column(String(100), default="Mumbai")
    area_type = Column(String(50), default="rural") # rural, urban
    pincode = Column(String(20), default="400001")
    
    profile_completed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")

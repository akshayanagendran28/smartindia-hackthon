import os

base = "C:/Users/aksha/.gemini/antigravity/scratch/scheme-sathi/backend"

def save(rel_path, content):
    full_path = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

# requirements.txt
save("requirements.txt", """fastapi>=0.110.0
uvicorn>=0.28.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
sqlalchemy>=2.0.25
python-multipart>=0.0.9
PyJWT>=2.8.0
bcrypt>=4.1.0
httpx>=0.27.0
python-dotenv>=1.0.0
pillow>=10.2.0
pandas>=2.2.0
numpy>=1.26.0
scikit-learn>=1.4.0
""")

save("app/__init__.py", "")
save("app/database/__init__.py", "")
save("app/models/__init__.py", """from app.models.user import User, UserProfile
from app.models.scheme import Scheme, SchemeVersion, SchemeRule, SchemeDocument
from app.models.partner import ChannelPartner, PartnerScheme
from app.models.application import UserDocument, Recommendation, SavedScheme, Notification, ChatSession, ChatMessage
""")

# app/config.py
save("app/config.py", """import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "SCHEME SATHI API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "scheme-sathi-sih26092-super-secret-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # SQLite local zero-config default, easily overridden with Postgres / PostGIS
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./scheme_sathi.db")
    
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE_MB: int = 15
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    class Config:
        case_sensitive = True

settings = Settings()
""")

# app/database/session.py
save("app/database/session.py", """import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

# app/models/user.py
save("app/models/user.py", """import datetime
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
    
    # Personal
    age = Column(Integer, nullable=True)
    gender = Column(String(30), nullable=True) # Male, Female, Other
    category = Column(String(50), default="General") # General, SC, ST, OBC, Minority, Woman, EWS, Divyangjan
    
    # Financial
    annual_family_income = Column(Float, default=0.0)
    existing_loans = Column(Float, default=0.0)
    
    # Business
    is_new_business = Column(Boolean, default=True)
    business_type = Column(String(100), default="Micro Retail") # Manufacturing, Service, Trading, Agriculture & Allied, Artisan / Handicraft, Micro Retail, Technology / Innovation
    gstin = Column(String(50), nullable=True)
    project_cost = Column(Float, default=0.0)
    required_loan_amount = Column(Float, default=0.0)
    purpose = Column(String(100), default="Start a Business") # Start a Business, Expand Existing Business, Small Project Loan, Large Project / Term Loan, Education Loan, Working Capital
    
    # Education
    is_student = Column(Boolean, default=False)
    course = Column(String(200), nullable=True)
    institution = Column(String(200), nullable=True)
    education_cost = Column(Float, default=0.0)
    
    # Location
    location_state = Column(String(100), nullable=True)
    location_district = Column(String(100), nullable=True)
    pincode = Column(String(20), nullable=True)
    
    profile_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")
""")

# app/models/scheme.py
save("app/models/scheme.py", """import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.database.session import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    category = Column(String(100), default="Credit & Loan") # Credit & Loan, Subsidy, Education, Women, SC/ST, Artisan
    description = Column(Text, nullable=False)
    loan_type = Column(String(100), default="Term Loan / Working Capital")
    
    # Quantitative thresholds
    min_loan_amount = Column(Float, default=10000.0)
    max_loan_amount = Column(Float, default=1000000.0)
    min_project_cost = Column(Float, default=10000.0)
    max_project_cost = Column(Float, default=5000000.0)
    min_age = Column(Integer, default=18)
    max_age = Column(Integer, default=65)
    max_income_limit = Column(Float, nullable=True) # None = No ceiling
    
    # Financial Terms
    interest_rate_min = Column(Float, default=7.0)
    interest_rate_max = Column(Float, default=12.0)
    interest_rate_display = Column(String(100), default="7.0% - 11.5% p.a. (Subsidized)")
    repayment_period_months = Column(Integer, default=60) # Tenure
    moratorium_months = Column(Integer, default=6)
    subsidy_percentage_general = Column(Float, default=15.0)
    subsidy_percentage_special = Column(Float, default=25.0) # For SC/ST/Women/NER/Rural
    subsidy_details = Column(Text, nullable=True)
    
    # JSON-encoded array strings for compatibility check
    eligible_purposes = Column(Text, default='["Start a Business", "Expand Existing Business"]')
    eligible_business_types = Column(Text, default='["Manufacturing", "Service", "Trading", "Micro Retail"]')
    eligible_categories = Column(Text, default='["General", "SC", "ST", "OBC", "Minority", "Woman", "EWS", "Divyangjan"]')
    eligible_states = Column(Text, default='["All India"]')
    eligible_education = Column(Text, default='[]')
    
    is_active = Column(Boolean, default=True)
    official_portal_url = Column(String(500), nullable=True)
    application_process = Column(Text, nullable=True)
    version = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    rules = relationship("SchemeRule", back_populates="scheme", cascade="all, delete-orphan")
    documents = relationship("SchemeDocument", back_populates="scheme", cascade="all, delete-orphan")
    versions = relationship("SchemeVersion", back_populates="scheme", cascade="all, delete-orphan")
    partner_associations = relationship("PartnerScheme", back_populates="scheme", cascade="all, delete-orphan")

class SchemeVersion(Base):
    __tablename__ = "scheme_versions"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    effective_from = Column(DateTime, default=datetime.datetime.utcnow)
    change_summary = Column(Text, nullable=False)
    rules_snapshot = Column(Text, nullable=True) # JSON snapshot
    scheme_snapshot = Column(Text, nullable=True) # Full JSON dump
    updated_by = Column(String(100), default="Admin")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    scheme = relationship("Scheme", back_populates="versions")

class SchemeRule(Base):
    __tablename__ = "scheme_rules"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    rule_name = Column(String(200), nullable=False)
    rule_code = Column(String(100), nullable=False)
    field_name = Column(String(100), nullable=False)
    operator = Column(String(30), nullable=False) # <=, >=, ==, !=, in, contains, max_limit, min_limit
    threshold_value = Column(String(500), nullable=False)
    rule_type = Column(String(50), default="hard_eligibility") # hard_eligibility, soft_preference
    weight = Column(Float, default=1.0)
    failure_reason_template = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)

    scheme = relationship("Scheme", back_populates="rules")

class SchemeDocument(Base):
    __tablename__ = "scheme_documents"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    document_name = Column(String(200), nullable=False)
    document_type = Column(String(100), nullable=False) # aadhaar, income_certificate, caste_certificate, business_proof, bank_statement, project_report, gst_certificate, education_proof
    is_mandatory = Column(Boolean, default=True)
    description = Column(String(500), nullable=True)

    scheme = relationship("Scheme", back_populates="documents")
""")

# app/models/partner.py
save("app/models/partner.py", """import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.database.session import Base

class ChannelPartner(Base):
    __tablename__ = "channel_partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    partner_type = Column(String(100), default="Lead District Bank")
    address = Column(Text, nullable=False)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact_person = Column(String(150), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    contact_email = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    verification_status = Column(String(50), default="verified") # verified, pending, partner
    supported_scheme_codes = Column(Text, default="[]")
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    schemes = relationship("PartnerScheme", back_populates="partner", cascade="all, delete-orphan")

class PartnerScheme(Base):
    __tablename__ = "partner_schemes"

    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("channel_partners.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)

    partner = relationship("ChannelPartner", back_populates="schemes")
    scheme = relationship("Scheme", back_populates="partner_associations")
""")

# app/models/application.py
save("app/models/application.py", """import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.database.session import Base

class UserDocument(Base):
    __tablename__ = "user_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_type = Column(String(100), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    extracted_data = Column(Text, default="{}")
    verification_status = Column(String(50), default="extracted") # extracted, needs_review, verified, mismatch
    mismatch_details = Column(Text, default="[]")
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="documents")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    match_score = Column(Float, default=0.0) # 0 to 100
    is_eligible = Column(Boolean, default=True)
    eligibility_status = Column(String(50), default="eligible") # eligible, partially_eligible, ineligible
    compatibility_breakdown = Column(Text, default="{}") # JSON: income, purpose, loan, project_cost, location, business
    matching_factors = Column(Text, default="[]")
    missing_requirements = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="recommendations")
    scheme = relationship("Scheme")

class SavedScheme(Base):
    __tablename__ = "saved_schemes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    notes = Column(Text, nullable=True)
    saved_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="saved_schemes")
    scheme = relationship("Scheme")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="scheme_match") # scheme_match, doc_missing, scheme_update, partner_alert
    is_read = Column(Boolean, default=False)
    link = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="notifications")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    language = Column(String(20), default="en")
    session_title = Column(String(255), default="New Conversation")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String(20), default="user") # user, assistant
    text = Column(Text, nullable=False)
    language = Column(String(20), default="en")
    extracted_intent = Column(Text, default="{}")
    recommendations_payload = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
""")

print("Models and Config generated successfully!")

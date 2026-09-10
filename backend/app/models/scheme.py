import datetime
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
    purpose_type = Column(String(50), default="BUSINESS", index=True) # BUSINESS, EDUCATION, SELF_EMPLOYMENT
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

    @property
    def ministry(self):
        return self.department

    @property
    def target_category(self):
        return self.category

    @property
    def moratorium_period_months(self):
        return self.moratorium_months

    @property
    def required_documents(self):
        if self.documents:
            return [d.document_name for d in self.documents]
        return ["Aadhaar Card", "PAN Card", "Caste Certificate", "Project Report", "Bank Passbook"]

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

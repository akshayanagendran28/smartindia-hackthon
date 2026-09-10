import datetime
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
    verification_status = Column(String(50), default="extracted") # extracted, verified, mismatch, needs_review, format_invalid
    mismatch_details = Column(Text, default="[]")
    ocr_status = Column(String(50), default="SUCCESS")
    format_valid = Column(Boolean, default=True)
    profile_match = Column(Boolean, default=True)
    official_verification = Column(String(50), default="VERIFIED")
    confidence_score = Column(Float, default=0.95)
    masked_identifier = Column(String(100), nullable=True)
    validation_checks = Column(Text, default="[]")
    audit_logs = Column(Text, default="[]")
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

class SchemeApplication(Base):
    __tablename__ = "scheme_applications"

    id = Column(Integer, primary_key=True, index=True)
    application_number = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("channel_partners.id"), nullable=True)

    purpose_type = Column(String(50), default="BUSINESS", index=True) # BUSINESS, EDUCATION, SELF_EMPLOYMENT
    loan_amount = Column(Float, nullable=False, default=1200000.0) # Single Source of Truth
    tenure_months = Column(Integer, default=60)
    moratorium_months = Column(Integer, default=6)
    interest_rate = Column(Float, default=8.5)
    subsidy_amount = Column(Float, default=0.0)
    calculated_emi = Column(Float, default=0.0)

    # Status: DRAFT, SUBMITTED, INVITATION_SENT, PARTNER_ASSIGNED, UNDER_REVIEW, SANCTIONED, REJECTED
    status = Column(String(50), default="SUBMITTED", index=True)
    invitation_status = Column(String(50), default="NONE", index=True) # NONE, PENDING, ACCEPTED, REJECTED
    
    applicant_data = Column(Text, default="{}") # JSON: Demographics, Course/Business details
    verified_documents = Column(Text, default="[]") # JSON array of verified doc keys
    status_history = Column(Text, default="[]") # JSON array of {status, timestamp, title, description, updated_by}
    partner_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User")
    scheme = relationship("Scheme")
    partner = relationship("ChannelPartner")
    invitations = relationship("PartnerInvitation", back_populates="application", cascade="all, delete-orphan")

class PartnerInvitation(Base):
    __tablename__ = "partner_invitations"

    id = Column(Integer, primary_key=True, index=True)
    invitation_number = Column(String(100), unique=True, index=True, nullable=False)
    application_id = Column(Integer, ForeignKey("scheme_applications.id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("channel_partners.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    status = Column(String(50), default="PENDING", index=True) # PENDING, ACCEPTED, REJECTED, EXPIRED
    response_notes = Column(Text, nullable=True)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)

    application = relationship("SchemeApplication", back_populates="invitations")
    partner = relationship("ChannelPartner")
    user = relationship("User")

import datetime
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

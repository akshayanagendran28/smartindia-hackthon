from pydantic import BaseModel
from typing import Optional, List
import datetime

class ChannelPartnerOut(BaseModel):
    id: int
    name: str
    partner_type: str
    address: str
    state: str
    district: str
    pincode: Optional[str] = None
    latitude: float
    longitude: float
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    verification_status: str
    supported_scheme_codes: List[str] = []
    
    # Distance & Suitability
    distance_km: Optional[float] = None
    scheme_compatibility_score: Optional[float] = None
    partner_suitability_score: Optional[float] = None
    suitability_reason: Optional[str] = None

    class Config:
        from_attributes = True

class ChannelPartnerCreate(BaseModel):
    name: str
    partner_type: str
    address: str
    state: str
    district: str
    pincode: Optional[str] = None
    latitude: float
    longitude: float
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    verification_status: str = "verified"
    supported_scheme_codes: List[str] = []

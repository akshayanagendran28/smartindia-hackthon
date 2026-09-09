import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.partner import ChannelPartner
from app.schemas.partner import ChannelPartnerOut
from app.services.geo import GeospatialPartnerService

router = APIRouter(prefix="/partners", tags=["Channel Partner Locator & Map"])

@router.get("", response_model=List[ChannelPartnerOut])
def list_partners(
    state: Optional[str] = None,
    district: Optional[str] = None,
    partner_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ChannelPartner).filter(ChannelPartner.is_active == True)
    if state:
        query = query.filter(ChannelPartner.state.ilike(f"%{state}%"))
    if district:
        query = query.filter(ChannelPartner.district.ilike(f"%{district}%"))
    if partner_type:
        query = query.filter(ChannelPartner.partner_type == partner_type)
    
    partners = query.all()
    results = []
    for p in partners:
        try:
            codes = json.loads(p.supported_scheme_codes)
        except Exception:
            codes = []
        results.append(ChannelPartnerOut(
            id=p.id,
            name=p.name,
            partner_type=p.partner_type,
            address=p.address,
            state=p.state,
            district=p.district,
            pincode=p.pincode,
            latitude=p.latitude,
            longitude=p.longitude,
            contact_person=p.contact_person,
            contact_phone=p.contact_phone,
            contact_email=p.contact_email,
            website=p.website,
            verification_status=p.verification_status,
            supported_scheme_codes=codes
        ))
    return results

@router.get("/recommended", response_model=List[ChannelPartnerOut])
def get_recommended_partners(
    lat: float = Query(19.0760, description="Latitude (Default Mumbai)"),
    lon: float = Query(72.8777, description="Longitude (Default Mumbai)"),
    scheme_code: Optional[str] = Query(None, description="Target scheme code e.g. PMEGP"),
    db: Session = Depends(get_db)
):
    partners = db.query(ChannelPartner).filter(ChannelPartner.is_active == True).all()
    evaluated = []

    for p in partners:
        res = GeospatialPartnerService.evaluate_partner(p, lat, lon, scheme_code)
        evaluated.append(ChannelPartnerOut(**res))

    # Rank by combined partner suitability score descending
    evaluated.sort(key=lambda x: x.partner_suitability_score or 0.0, reverse=True)
    return evaluated

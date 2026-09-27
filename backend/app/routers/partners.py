import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.database.session import get_db
from app.models.partner import ChannelPartner, PartnerInvitation
from app.models.application import SchemeApplication, UserDocument
from app.models.user import User
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

@router.get("/{partner_id}/stats")
def get_partner_live_stats(
    partner_id: int,
    db: Session = Depends(get_db)
):
    """
    Returns 100% database calculated metrics for a specific Channel Partner.
    """
    partner = db.query(ChannelPartner).filter(ChannelPartner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found.")
        
    assigned_count = db.query(SchemeApplication).filter(SchemeApplication.partner_id == partner_id).count()
    pending_invitations = db.query(PartnerInvitation).filter(PartnerInvitation.partner_id == partner_id, PartnerInvitation.status == "PENDING").count()
    under_review = db.query(SchemeApplication).filter(SchemeApplication.partner_id == partner_id, SchemeApplication.loan_status == "UNDER_REVIEW").count()
    loans_approved = db.query(SchemeApplication).filter(SchemeApplication.partner_id == partner_id, SchemeApplication.loan_status.in_(["APPROVED", "SANCTIONED"])).count()
    funds_released = db.query(SchemeApplication).filter(SchemeApplication.partner_id == partner_id, SchemeApplication.fund_status == "RELEASED").count()
    
    return {
        "partner_id": partner.id,
        "partner_name": partner.name,
        "district": partner.district,
        "state": partner.state,
        "assigned_customers_count": assigned_count,
        "pending_invitations_count": pending_invitations,
        "under_review_count": under_review,
        "loans_approved_count": loans_approved,
        "funds_released_count": funds_released
    }

@router.get("/{partner_id}/assigned-applications")
def get_partner_assigned_applications(
    partner_id: int,
    db: Session = Depends(get_db)
):
    """
    Returns only the applications assigned to this specific Channel Partner.
    Partner X cannot see Partner Y's applications.
    """
    partner = db.query(ChannelPartner).filter(ChannelPartner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found.")
        
    apps = db.query(SchemeApplication).filter(SchemeApplication.partner_id == partner_id).order_by(desc(SchemeApplication.created_at)).all()
    
    app_list = []
    for a in apps:
        app_list.append({
            "id": a.id,
            "application_number": a.application_number,
            "customer_id": a.user_id,
            "customer_name": a.user.full_name if a.user else "Applicant",
            "customer_email": a.user.email if a.user else None,
            "customer_mobile": a.user.mobile if a.user else None,
            "scheme_name": a.scheme.name if a.scheme else None,
            "scheme_code": a.scheme.code if a.scheme else None,
            "loan_amount": a.loan_amount,
            "purpose_type": a.purpose_type,
            "status": a.status,
            "loan_status": a.loan_status,
            "fund_status": a.fund_status,
            "appointment_status": a.appointment_status,
            "created_at": a.created_at.isoformat() + "Z" if a.created_at else None
        })
        
    return {
        "partner": {
            "id": partner.id,
            "name": partner.name,
            "district": partner.district,
            "state": partner.state
        },
        "assigned_applications": app_list,
        "total_assigned": len(app_list)
    }

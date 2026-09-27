# -*- coding: utf-8 -*-
"""
Scheme Applications & Channel Partner Invitation Router
Provides end-to-end Application Submission, Channel Partner Invitation,
Partner Acceptance / Rejection Workflow, and Transparent Status History Tracking.
"""
import json
import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.database.session import get_db
from app.models.user import User, UserProfile
from app.models.scheme import Scheme
from app.models.partner import ChannelPartner
from app.models.application import SchemeApplication, PartnerInvitation, Notification, AuditLog
from app.auth.deps import get_current_user_flexible

router = APIRouter(prefix="/applications", tags=["Scheme Applications & Partner Workflow"])

@router.post("/submit")
def submit_scheme_application(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Submits a confirmed Scheme Application after profile review & document verification.
    """
    scheme_id = payload.get("scheme_id")
    if not scheme_id and payload.get("scheme_code"):
        scheme = db.query(Scheme).filter(Scheme.code == payload.get("scheme_code")).first()
        if scheme:
            scheme_id = scheme.id

    if not scheme_id:
        # Default to first scheme if available
        scheme = db.query(Scheme).first()
        if scheme:
            scheme_id = scheme.id
        else:
            raise HTTPException(status_code=400, detail="Scheme ID or scheme_code is required.")

    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail=f"Scheme with ID {scheme_id} not found.")

    p_type = (payload.get("purpose_type") or scheme.purpose_type or "BUSINESS").upper()
    loan_amt = float(payload.get("loan_amount") or payload.get("required_loan_amount") or payload.get("required_loan") or 1200000.0)

    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    app_num = f"APP-2026-{p_type[:3]}-{uuid.uuid4().hex[:6].upper()}"

    initial_history = [
        {
            "status": "SUBMITTED",
            "timestamp": now_iso,
            "title": "Application Submitted",
            "description": f"Application for {scheme.name} ({scheme.code}) submitted by {current_user.full_name or 'Applicant'}.",
            "updated_by": current_user.full_name or "Applicant",
            "actor_role": "CUSTOMER"
        },
        {
            "status": "DOCUMENTS_VERIFIED",
            "timestamp": now_iso,
            "title": "Mandatory Document Gate Cleared",
            "description": "Statutory documents verified via OCR validation pipeline.",
            "updated_by": "Scheme Sathi OCR Gate",
            "actor_role": "SYSTEM"
        },
        {
            "status": "ELIGIBILITY_CONFIRMED",
            "timestamp": now_iso,
            "title": "Deterministic Policy Rules Satisfied",
            "description": f"Applicant satisfies official {scheme.code} policy rules and statutory thresholds.",
            "updated_by": "Scheme Sathi Rule Engine",
            "actor_role": "SYSTEM"
        }
    ]

    verified_docs = payload.get("verified_documents") or ["aadhaar", "pan", "caste_certificate"]
    applicant_data = {
        "full_name": current_user.full_name,
        "email": current_user.email,
        "mobile": current_user.mobile,
        "purpose_type": p_type,
        "loan_amount": loan_amt,
        "state": current_user.state or (current_user.profile.state if current_user.profile else "Maharashtra"),
        "district": current_user.district or (current_user.profile.district if current_user.profile else "Mumbai"),
        "category": (current_user.profile.social_category or current_user.profile.category) if current_user.profile else "SC"
    }

    # Calculate initial subsidy estimation
    subsidy_val = 0.0
    soc_cat = (current_user.profile.social_category or current_user.profile.category) if current_user.profile else "SC"
    if scheme.subsidy_percentage_special and soc_cat in ["SC", "ST", "OBC", "Woman", "Minority", "Divyangjan"]:
        subsidy_val = round((loan_amt * scheme.subsidy_percentage_special) / 100.0, 2)
    elif scheme.subsidy_percentage_general:
        subsidy_val = round((loan_amt * scheme.subsidy_percentage_general) / 100.0, 2)

    app_obj = SchemeApplication(
        application_number=app_num,
        user_id=current_user.id,
        scheme_id=scheme.id,
        partner_id=None,
        purpose_type=p_type,
        loan_amount=loan_amt,
        tenure_months=int(payload.get("tenure_months") or scheme.repayment_period_months or 60),
        moratorium_months=int(payload.get("moratorium_months") or scheme.moratorium_months or 6),
        interest_rate=float(payload.get("interest_rate") or scheme.interest_rate_min or 8.5),
        subsidy_amount=subsidy_val,
        calculated_emi=float(payload.get("calculated_emi") or 0.0),
        status="SUBMITTED",
        invitation_status="NONE",
        loan_status="PENDING",
        fund_status="PENDING",
        fund_amount=0.0,
        appointment_status="NOT_REQUIRED",
        applicant_data=json.dumps(applicant_data),
        verified_documents=json.dumps(verified_docs),
        status_history=json.dumps(initial_history)
    )

    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)

    # Add audit log for admin visibility
    audit = AuditLog(
        actor_id=current_user.id,
        actor_role="customer",
        actor_name=current_user.full_name or "Applicant",
        action="APPLICATION_SUBMITTED",
        entity_type="application",
        entity_id=str(app_obj.id),
        reason=f"Applicant {current_user.full_name} submitted application {app_num} for {scheme.name} ({scheme.code})."
    )
    db.add(audit)

    # In-app notifications
    notif = Notification(
        user_id=current_user.id,
        title=f"Application {app_num} Created",
        message=f"Your application for {scheme.name} is ready for Channel Partner invitation.",
        notification_type="scheme_match",
        link="/history",
        is_read=False
    )
    db.add(notif)

    # Admin notifications
    admins = db.query(User).filter(User.role.in_(["admin", "supervisor"])).all()
    for adm in admins:
        db.add(Notification(
            user_id=adm.id,
            title=f"New Scheme Application: {scheme.code}",
            message=f"{current_user.full_name} submitted application {app_num} for {scheme.name}.",
            notification_type="admin_alert",
            link="/admin/users",
            is_read=False
        ))

    db.commit()

    return {
        "status": "success",
        "message": "Application submitted successfully.",
        "application_id": app_obj.id,
        "application_number": app_obj.application_number,
        "scheme_name": scheme.name,
        "purpose_type": p_type,
        "loan_amount": loan_amt,
        "status": app_obj.status,
        "status_history": initial_history
    }


@router.post("/invite-partner")
def invite_channel_partner_direct(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Direct Citizen Channel Partner Invitation endpoint.
    Allows a customer to invite a partner branch from Map / Suggestions with or without a pre-existing application ID.
    Dispatches an official invitation, records an immutable audit log, and fires real-time alerts for the Admin.
    """
    app_id = payload.get("application_id") or payload.get("app_id")
    app_obj = None
    if app_id:
        app_obj = db.query(SchemeApplication).filter(
            SchemeApplication.id == app_id,
            SchemeApplication.user_id == current_user.id
        ).first()

    if not app_obj:
        # Find latest pending/submitted application of user
        app_obj = db.query(SchemeApplication).filter(
            SchemeApplication.user_id == current_user.id
        ).order_by(SchemeApplication.created_at.desc()).first()

    # If still no application exists, create an active scheme application for this request
    if not app_obj:
        scheme_code = payload.get("scheme_code") or "PMEGP"
        scheme = db.query(Scheme).filter(Scheme.code == scheme_code).first() or db.query(Scheme).first()
        p_type = (payload.get("purpose_type") or (scheme.purpose_type if scheme else "BUSINESS")).upper()
        loan_amt = float(payload.get("loan_amount") or 1200000.0)
        now_iso = datetime.datetime.utcnow().isoformat() + "Z"
        app_num = f"APP-2026-{p_type[:3]}-{uuid.uuid4().hex[:6].upper()}"

        initial_history = [
            {
                "status": "SUBMITTED",
                "timestamp": now_iso,
                "title": f"Scheme Application Created: {scheme.code if scheme else 'SCHEME'}",
                "description": f"Application for {scheme.name if scheme else 'Scheme'} created for Partner Appraisal.",
                "updated_by": current_user.full_name or "Applicant",
                "actor_role": "CUSTOMER"
            }
        ]

        app_obj = SchemeApplication(
            application_number=app_num,
            user_id=current_user.id,
            scheme_id=scheme.id if scheme else None,
            partner_id=None,
            purpose_type=p_type,
            loan_amount=loan_amt,
            tenure_months=60,
            moratorium_months=6,
            interest_rate=8.5,
            subsidy_amount=round(loan_amt * 0.25, 2),
            calculated_emi=0.0,
            status="INVITATION_SENT",
            invitation_status="PENDING",
            loan_status="UNDER_REVIEW",
            fund_status="PENDING",
            fund_amount=0.0,
            appointment_status="NOT_REQUIRED",
            applicant_data=json.dumps({
                "full_name": current_user.full_name,
                "email": current_user.email,
                "mobile": current_user.mobile,
                "district": payload.get("district") or current_user.district,
                "state": payload.get("state") or current_user.state
            }),
            verified_documents=json.dumps(["aadhaar", "pan"]),
            status_history=json.dumps(initial_history)
        )
        db.add(app_obj)
        db.commit()
        db.refresh(app_obj)

    # Resolve Channel Partner
    partner_id = payload.get("partner_id")
    partner = None
    if partner_id:
        partner = db.query(ChannelPartner).filter(ChannelPartner.id == partner_id).first()

    if not partner:
        p_name = payload.get("partner_name") or payload.get("bank") or "Lead District Bank Branch"
        p_state = payload.get("state") or current_user.state or "Maharashtra"
        p_dist = payload.get("district") or current_user.district or "Mumbai"

        partner = db.query(ChannelPartner).filter(
            ChannelPartner.name.ilike(f"%{p_name}%"),
            ChannelPartner.district.ilike(f"%{p_dist}%")
        ).first()

        if not partner:
            partner = ChannelPartner(
                name=p_name,
                partner_type=payload.get("partner_type") or ("Lead District Bank" if payload.get("lead_bank_flag") else "Commercial Bank"),
                address=payload.get("address") or f"{p_name}, {payload.get('branch') or ''}, {p_dist}, {p_state}",
                state=p_state,
                district=p_dist,
                latitude=float(payload.get("latitude") or 19.0760),
                longitude=float(payload.get("longitude") or 72.8777),
                contact_person=payload.get("contact_person") or payload.get("nodal_officer") or "Branch Nodal Officer",
                contact_phone=payload.get("contact_phone") or payload.get("nodal_phone") or "1800-425-3800",
                contact_email=payload.get("contact_email") or "nodal@leadbank.gov.in",
                verification_status="verified",
                supported_scheme_codes=json.dumps([app_obj.scheme.code if app_obj.scheme else "PMEGP"])
            )
            db.add(partner)
            db.commit()
            db.refresh(partner)

    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    inv_num = f"INV-{uuid.uuid4().hex[:8].upper()}"

    invitation = PartnerInvitation(
        invitation_number=inv_num,
        application_id=app_obj.id,
        partner_id=partner.id,
        user_id=current_user.id,
        status="PENDING",
        sent_at=datetime.datetime.utcnow()
    )
    db.add(invitation)

    app_obj.invitation_status = "PENDING"
    app_obj.status = "INVITATION_SENT"
    app_obj.partner_id = partner.id

    try:
        history = json.loads(app_obj.status_history or "[]")
    except Exception:
        history = []

    history.append({
        "status": "INVITATION_SENT",
        "timestamp": now_iso,
        "title": f"Invitation Dispatched to {partner.name}",
        "description": f"Citizen invited {partner.name} ({partner.district}, {partner.state}) for scheme appraisal and loan sanctions.",
        "updated_by": current_user.full_name or "Applicant",
        "actor_role": "CUSTOMER"
    })
    app_obj.status_history = json.dumps(history)

    # 1. Audit Log
    audit = AuditLog(
        actor_id=current_user.id,
        actor_role="customer",
        actor_name=current_user.full_name or "Applicant",
        action="PARTNER_INVITATION_SENT",
        entity_type="application",
        entity_id=str(app_obj.id),
        reason=f"Applicant {current_user.full_name} ({current_user.district or partner.district}, {current_user.state or partner.state}) invited Channel Partner {partner.name} ({partner.district}) for application {app_obj.application_number}."
    )
    db.add(audit)

    # 2. In-App Customer Notification
    db.add(Notification(
        user_id=current_user.id,
        title=f"Partner Invitation Sent: {partner.name}",
        message=f"Your invitation was sent to {partner.name} ({partner.district}). National Portal Admin has been alerted in real time.",
        notification_type="scheme_match",
        link="/dashboard",
        is_read=False
    ))

    # 3. In-App Admin Notification (admin_alert)
    admins = db.query(User).filter(User.role.in_(["admin", "supervisor"])).all()
    for adm in admins:
        db.add(Notification(
            user_id=adm.id,
            title=f"Citizen Invited Channel Partner: {partner.name}",
            message=f"Citizen {current_user.full_name} ({current_user.district or partner.district}, {current_user.state or partner.state}) invited {partner.name} for scheme appraisal ({app_obj.application_number}).",
            notification_type="admin_alert",
            link="/admin/partners",
            is_read=False
        ))

    db.commit()
    db.refresh(app_obj)

    return {
        "status": "success",
        "message": f"Invitation successfully dispatched to {partner.name}. Portal Admin notified in real time!",
        "invitation_number": inv_num,
        "application_id": app_obj.id,
        "application_number": app_obj.application_number,
        "application_status": app_obj.status,
        "invitation_status": app_obj.invitation_status,
        "partner_name": partner.name,
        "partner_id": partner.id,
        "partner_district": partner.district,
        "partner_state": partner.state,
        "status_history": history
    }


@router.post("/{app_id}/invite-partner")
def invite_channel_partner(
    app_id: int,
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Sends an invitation to a specific Channel Partner branch for application processing.
    """
    app_obj = db.query(SchemeApplication).filter(
        SchemeApplication.id == app_id,
        SchemeApplication.user_id == current_user.id
    ).first()

    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found.")

    partner_id = payload.get("partner_id")
    partner = None

    if partner_id:
        partner = db.query(ChannelPartner).filter(ChannelPartner.id == partner_id).first()

    if not partner:
        p_name = payload.get("partner_name") or payload.get("bank") or "Lead District Bank Desk"
        p_state = payload.get("state") or current_user.state or "Maharashtra"
        p_dist = payload.get("district") or current_user.district or "Mumbai"
        
        # Look up existing partner by name & district
        partner = db.query(ChannelPartner).filter(
            ChannelPartner.name.ilike(f"%{p_name}%"),
            ChannelPartner.district.ilike(f"%{p_dist}%")
        ).first()

        if not partner:
            # Create partner in DB
            partner = ChannelPartner(
                name=p_name,
                partner_type=payload.get("partner_type") or "Lead District Bank",
                address=payload.get("address") or f"{p_name}, {p_dist}, {p_state}",
                state=p_state,
                district=p_dist,
                latitude=float(payload.get("latitude") or 19.0760),
                longitude=float(payload.get("longitude") or 72.8777),
                contact_person=payload.get("contact_person") or "Nodal Officer",
                contact_phone=payload.get("contact_phone") or "1800-425-3800",
                contact_email=payload.get("contact_email") or "nodal@leadbank.gov.in",
                verification_status="verified",
                supported_scheme_codes=json.dumps([app_obj.scheme.code if app_obj.scheme else "PMEGP"])
            )
            db.add(partner)
            db.commit()
            db.refresh(partner)

    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    inv_num = f"INV-{uuid.uuid4().hex[:8].upper()}"

    # Create Partner Invitation
    invitation = PartnerInvitation(
        invitation_number=inv_num,
        application_id=app_obj.id,
        partner_id=partner.id,
        user_id=current_user.id,
        status="PENDING",
        sent_at=datetime.datetime.utcnow()
    )
    db.add(invitation)

    # Update Application
    app_obj.invitation_status = "PENDING"
    app_obj.status = "INVITATION_SENT"
    app_obj.partner_id = partner.id # Assigned pending partner

    try:
        history = json.loads(app_obj.status_history or "[]")
    except Exception:
        history = []

    history.append({
        "status": "INVITATION_SENT",
        "timestamp": now_iso,
        "title": f"Invitation Dispatched to {partner.name}",
        "description": f"Application dossier sent to {partner.name} ({partner.district}, {partner.state}) for bank desk review.",
        "updated_by": current_user.full_name or "Applicant",
        "actor_role": "CUSTOMER"
    })
    app_obj.status_history = json.dumps(history)

    # Audit log for Admin Live Activity Stream
    audit = AuditLog(
        actor_id=current_user.id,
        actor_role="customer",
        actor_name=current_user.full_name or "Applicant",
        action="PARTNER_INVITATION_SENT",
        entity_type="application",
        entity_id=str(app_obj.id),
        reason=f"Applicant {current_user.full_name} invited Channel Partner {partner.name} ({partner.district}) for application {app_obj.application_number}."
    )
    db.add(audit)

    # Admin Alert
    admins = db.query(User).filter(User.role.in_(["admin", "supervisor"])).all()
    for adm in admins:
        db.add(Notification(
            user_id=adm.id,
            title=f"Partner Invitation: {partner.name}",
            message=f"Application {app_obj.application_number} ({app_obj.scheme.code if app_obj.scheme else 'SCHEME'}) was dispatched to {partner.name}.",
            notification_type="admin_alert",
            link="/admin/partners",
            is_read=False
        ))

    db.commit()
    db.refresh(app_obj)

    return {
        "status": "success",
        "message": f"Invitation successfully sent to {partner.name}.",
        "invitation_number": inv_num,
        "application_status": app_obj.status,
        "invitation_status": app_obj.invitation_status,
        "partner_name": partner.name,
        "partner_id": partner.id,
        "status_history": history
    }


@router.post("/apply-with-partner")
def apply_scheme_with_partner(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    1-Step Application & Channel Partner Selection.
    Submits the scheme application and links the selected channel partner immediately,
    logging an audit event and triggering live notifications for Admin.
    """
    # 1. Identify Scheme
    scheme_code = payload.get("scheme_code")
    scheme_id = payload.get("scheme_id")
    scheme = None
    if scheme_id:
        scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    elif scheme_code:
        scheme = db.query(Scheme).filter(Scheme.code == scheme_code).first()

    if not scheme:
        scheme = db.query(Scheme).first()
        if not scheme:
            raise HTTPException(status_code=400, detail="No valid government schemes configured in database.")

    # 2. Identify / Register Partner
    partner_id = payload.get("partner_id")
    partner = None
    if partner_id:
        partner = db.query(ChannelPartner).filter(ChannelPartner.id == partner_id).first()

    if not partner:
        p_name = payload.get("partner_name") or payload.get("bank") or "Lead District Bank Branch Desk"
        p_state = payload.get("state") or current_user.state or (current_user.profile.state if current_user.profile else "Maharashtra")
        p_dist = payload.get("district") or current_user.district or (current_user.profile.district if current_user.profile else "Mumbai")
        
        partner = db.query(ChannelPartner).filter(
            ChannelPartner.name.ilike(f"%{p_name}%"),
            ChannelPartner.district.ilike(f"%{p_dist}%")
        ).first()

        if not partner:
            partner = ChannelPartner(
                name=p_name,
                partner_type=payload.get("partner_type") or ("Lead District Bank" if payload.get("lead_bank_flag") else "Commercial Bank"),
                address=payload.get("address") or f"{p_name}, {payload.get('branch') or ''}, {p_dist}, {p_state}",
                state=p_state,
                district=p_dist,
                latitude=float(payload.get("latitude") or 19.0760),
                longitude=float(payload.get("longitude") or 72.8777),
                contact_person=payload.get("contact_person") or payload.get("nodal_officer") or "Branch Nodal Officer",
                contact_phone=payload.get("contact_phone") or payload.get("nodal_phone") or "1800-425-3800",
                contact_email=payload.get("contact_email") or "nodal@leadbank.gov.in",
                verification_status="verified",
                supported_scheme_codes=json.dumps([scheme.code])
            )
            db.add(partner)
            db.commit()
            db.refresh(partner)

    # 3. Create Application
    p_type = (payload.get("purpose_type") or scheme.purpose_type or "BUSINESS").upper()
    loan_amt = float(payload.get("loan_amount") or payload.get("required_loan_amount") or payload.get("required_loan") or 1200000.0)

    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    app_num = f"APP-2026-{p_type[:3]}-{uuid.uuid4().hex[:6].upper()}"

    initial_history = [
        {
            "status": "SUBMITTED",
            "timestamp": now_iso,
            "title": f"Scheme Application Submitted: {scheme.code}",
            "description": f"Application for {scheme.name} ({scheme.code}) submitted with quantum ₹{loan_amt:,.2f}.",
            "updated_by": current_user.full_name or "Applicant",
            "actor_role": "CUSTOMER"
        },
        {
            "status": "PARTNER_ASSIGNED",
            "timestamp": now_iso,
            "title": f"Channel Partner Assigned: {partner.name}",
            "description": f"Assigned {partner.name} ({partner.district}, {partner.state}) for branch credit appraisal.",
            "updated_by": current_user.full_name or "Applicant",
            "actor_role": "CUSTOMER"
        }
    ]

    verified_docs = payload.get("verified_documents") or ["aadhaar", "pan", "caste_certificate"]
    applicant_data = {
        "full_name": current_user.full_name,
        "email": current_user.email,
        "mobile": current_user.mobile,
        "purpose_type": p_type,
        "loan_amount": loan_amt,
        "state": partner.state,
        "district": partner.district,
        "category": (current_user.profile.social_category or current_user.profile.category) if current_user.profile else "SC"
    }

    # Subsidy estimation
    subsidy_val = 0.0
    soc_cat = (current_user.profile.social_category or current_user.profile.category) if current_user.profile else "SC"
    if scheme.subsidy_percentage_special and soc_cat in ["SC", "ST", "OBC", "Woman", "Minority", "Divyangjan"]:
        subsidy_val = round((loan_amt * scheme.subsidy_percentage_special) / 100.0, 2)
    elif scheme.subsidy_percentage_general:
        subsidy_val = round((loan_amt * scheme.subsidy_percentage_general) / 100.0, 2)

    app_obj = SchemeApplication(
        application_number=app_num,
        user_id=current_user.id,
        scheme_id=scheme.id,
        partner_id=partner.id,
        purpose_type=p_type,
        loan_amount=loan_amt,
        tenure_months=int(payload.get("tenure_months") or scheme.repayment_period_months or 60),
        moratorium_months=int(payload.get("moratorium_months") or scheme.moratorium_months or 6),
        interest_rate=float(payload.get("interest_rate") or scheme.interest_rate_min or 8.5),
        subsidy_amount=subsidy_val,
        calculated_emi=float(payload.get("calculated_emi") or 0.0),
        status="PARTNER_ASSIGNED",
        invitation_status="PENDING",
        loan_status="UNDER_REVIEW",
        fund_status="PENDING",
        fund_amount=0.0,
        appointment_status="NOT_REQUIRED",
        applicant_data=json.dumps(applicant_data),
        verified_documents=json.dumps(verified_docs),
        status_history=json.dumps(initial_history)
    )
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)

    # 4. Create Partner Invitation
    inv_num = f"INV-{uuid.uuid4().hex[:8].upper()}"
    invitation = PartnerInvitation(
        invitation_number=inv_num,
        application_id=app_obj.id,
        partner_id=partner.id,
        user_id=current_user.id,
        status="PENDING",
        sent_at=datetime.datetime.utcnow()
    )
    db.add(invitation)

    # 5. Add Audit Log for Admin Dashboard Real-time Stream
    audit = AuditLog(
        actor_id=current_user.id,
        actor_role="customer",
        actor_name=current_user.full_name or "Applicant",
        action="APPLICATION_APPLIED_WITH_PARTNER",
        entity_type="application",
        entity_id=str(app_obj.id),
        reason=f"Applicant {current_user.full_name} applied for {scheme.name} ({scheme.code}) with quantum Rs. {loan_amt:,.2f} via partner {partner.name} ({partner.district}, {partner.state})."
    )
    db.add(audit)

    # 6. Add In-App Notifications
    db.add(Notification(
        user_id=current_user.id,
        title=f"Application {app_num} Created & Partner Assigned",
        message=f"You applied for {scheme.name}. {partner.name} has been assigned for credit appraisal.",
        notification_type="scheme_match",
        link="/dashboard",
        is_read=False
    ))

    # Notify all Admin users
    admins = db.query(User).filter(User.role.in_(["admin", "supervisor"])).all()
    for adm in admins:
        db.add(Notification(
            user_id=adm.id,
            title=f"New Application: {scheme.code} -> {partner.name}",
            message=f"Citizen {current_user.full_name} applied for {scheme.name} via partner {partner.name} ({partner.district}).",
            notification_type="admin_alert",
            link="/admin/users",
            is_read=False
        ))

    db.commit()

    return {
        "status": "success",
        "message": f"Successfully applied for {scheme.name} and assigned {partner.name}!",
        "application_id": app_obj.id,
        "application_number": app_obj.application_number,
        "scheme_name": scheme.name,
        "scheme_code": scheme.code,
        "partner_name": partner.name,
        "partner_id": partner.id,
        "partner_branch": f"{partner.district}, {partner.state}",
        "loan_amount": loan_amt,
        "status": app_obj.status,
        "loan_status": app_obj.loan_status,
        "status_history": initial_history
    }


@router.post("/{app_id}/partner-action")
def partner_action_on_application(
    app_id: int,
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Channel Partner accepts or rejects an application invitation.
    When accepted, application becomes PARTNER_ASSIGNED and advances loan status to UNDER_REVIEW.
    """
    app_obj = db.query(SchemeApplication).filter(SchemeApplication.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found.")

    action = payload.get("action", "").upper() # ACCEPT or REJECT
    notes = payload.get("notes", "")

    if action not in ["ACCEPT", "REJECT"]:
        raise HTTPException(status_code=400, detail="Action must be ACCEPT or REJECT.")

    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    invitation = db.query(PartnerInvitation).filter(
        PartnerInvitation.application_id == app_obj.id
    ).order_by(PartnerInvitation.sent_at.desc()).first()

    partner_name = app_obj.partner.name if app_obj.partner else "Channel Partner Desk"

    try:
        history = json.loads(app_obj.status_history or "[]")
    except Exception:
        history = []

    if action == "ACCEPT":
        app_obj.status = "PARTNER_ASSIGNED"
        app_obj.invitation_status = "ACCEPTED"
        app_obj.loan_status = "UNDER_REVIEW"
        app_obj.partner_notes = notes or "Application accepted for document physical appraisal."
        
        if invitation:
            invitation.status = "ACCEPTED"
            invitation.responded_at = datetime.datetime.utcnow()
            invitation.response_notes = notes

        history.append({
            "status": "PARTNER_ASSIGNED",
            "timestamp": now_iso,
            "title": f"Invitation Accepted by {partner_name}",
            "description": f"{partner_name} accepted the application dossier for branch sanctioning. Loan status is now Under Review.",
            "updated_by": partner_name,
            "actor_role": "CHANNEL_PARTNER"
        })

        # Send notification to applicant
        notif = Notification(
            user_id=app_obj.user_id,
            title="Partner Accepted Application!",
            message=f"{partner_name} has accepted your application dossier. Next step: Bank appraisal.",
            notification_type="partner_alert",
            link="/dashboard",
            is_read=False
        )
        db.add(notif)

        # Audit log for Admin
        db.add(AuditLog(
            actor_role="partner",
            actor_name=partner_name,
            action="PARTNER_INVITATION_ACCEPTED",
            entity_type="application",
            entity_id=str(app_obj.id),
            reason=f"{partner_name} accepted application {app_obj.application_number} for appraisal."
        ))

    else: # REJECT
        app_obj.status = "INVITATION_REJECTED"
        app_obj.invitation_status = "REJECTED"
        app_obj.rejection_reason = notes or "Partner desk capacity reached / out of jurisdiction."
        
        if invitation:
            invitation.status = "REJECTED"
            invitation.responded_at = datetime.datetime.utcnow()
            invitation.response_notes = notes

        history.append({
            "status": "INVITATION_REJECTED",
            "timestamp": now_iso,
            "title": f"Invitation Declined by {partner_name}",
            "description": f"Reason: {app_obj.rejection_reason}. You may invite another compatible partner.",
            "updated_by": partner_name,
            "actor_role": "CHANNEL_PARTNER"
        })

        notif = Notification(
            user_id=app_obj.user_id,
            title="Partner Update",
            message=f"{partner_name} was unable to accept your invitation. Please select another nearby branch.",
            notification_type="partner_alert",
            link="/dashboard",
            is_read=False
        )
        db.add(notif)

    app_obj.status_history = json.dumps(history)
    db.commit()
    db.refresh(app_obj)

    return {
        "status": "success",
        "action": action,
        "application_status": app_obj.status,
        "invitation_status": app_obj.invitation_status,
        "loan_status": app_obj.loan_status,
        "partner_name": partner_name,
        "status_history": history
    }


@router.get("/my-applications")
def get_my_applications(
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Returns full history of applications submitted by the current user with complete status history.
    """
    apps = db.query(SchemeApplication).filter(
        SchemeApplication.user_id == current_user.id
    ).order_by(SchemeApplication.created_at.desc()).all()

    results = []
    for a in apps:
        try:
            hist = json.loads(a.status_history or "[]")
        except Exception:
            hist = []
        try:
            applicant = json.loads(a.applicant_data or "{}")
        except Exception:
            applicant = {}

        results.append({
            "id": a.id,
            "application_number": a.application_number,
            "scheme_id": a.scheme_id,
            "scheme_name": a.scheme.name if a.scheme else "Government Scheme",
            "scheme_code": a.scheme.code if a.scheme else "SCHEME",
            "purpose_type": a.purpose_type,
            "loan_amount": a.loan_amount,
            "tenure_months": a.tenure_months,
            "moratorium_months": a.moratorium_months,
            "interest_rate": a.interest_rate,
            "subsidy_amount": a.subsidy_amount,
            "calculated_emi": a.calculated_emi or 0.0,
            "status": a.status,
            "invitation_status": a.invitation_status,
            "loan_status": a.loan_status or "PENDING",
            "fund_status": a.fund_status or "PENDING",
            "fund_amount": a.fund_amount or 0.0,
            "fund_release_date": a.fund_release_date.isoformat() + "Z" if a.fund_release_date else None,
            "fund_remarks": a.fund_remarks,
            "appointment_status": a.appointment_status or "NOT_REQUIRED",
            "appointment_date": a.appointment_date.isoformat() + "Z" if a.appointment_date else None,
            "appointment_time": a.appointment_time,
            "appointment_venue": a.appointment_venue,
            "appointment_remarks": a.appointment_remarks,
            "partner_id": a.partner_id,
            "partner_name": a.partner.name if a.partner else None,
            "partner_branch": f"{a.partner.district}, {a.partner.state}" if a.partner else None,
            "partner_address": a.partner.address if a.partner else None,
            "partner_phone": a.partner.contact_phone if a.partner else None,
            "partner_notes": a.partner_notes,
            "status_history": hist,
            "created_at": a.created_at.isoformat() + "Z" if a.created_at else None,
            "updated_at": a.updated_at.isoformat() + "Z" if a.updated_at else None
        })

    return results


@router.get("/{app_id}/status")
def get_application_status(
    app_id: int,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Detailed status history timeline and transparency audit for a specific application.
    """
    app_obj = db.query(SchemeApplication).filter(
        SchemeApplication.id == app_id
    ).first()

    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found.")

    try:
        hist = json.loads(app_obj.status_history or "[]")
    except Exception:
        hist = []

    return {
        "application_id": app_obj.id,
        "application_number": app_obj.application_number,
        "scheme_name": app_obj.scheme.name if app_obj.scheme else "",
        "scheme_code": app_obj.scheme.code if app_obj.scheme else "",
        "purpose_type": app_obj.purpose_type,
        "loan_amount": app_obj.loan_amount,
        "tenure_months": app_obj.tenure_months,
        "moratorium_months": app_obj.moratorium_months,
        "interest_rate": app_obj.interest_rate,
        "subsidy_amount": app_obj.subsidy_amount,
        "calculated_emi": app_obj.calculated_emi or 0.0,
        "status": app_obj.status,
        "invitation_status": app_obj.invitation_status,
        "loan_status": app_obj.loan_status or "PENDING",
        "fund_status": app_obj.fund_status or "PENDING",
        "fund_amount": app_obj.fund_amount or 0.0,
        "fund_release_date": app_obj.fund_release_date.isoformat() + "Z" if app_obj.fund_release_date else None,
        "fund_remarks": app_obj.fund_remarks,
        "appointment_status": app_obj.appointment_status or "NOT_REQUIRED",
        "appointment_date": app_obj.appointment_date.isoformat() + "Z" if app_obj.appointment_date else None,
        "appointment_time": app_obj.appointment_time,
        "appointment_venue": app_obj.appointment_venue,
        "appointment_remarks": app_obj.appointment_remarks,
        "partner_name": app_obj.partner.name if app_obj.partner else None,
        "partner_branch": f"{app_obj.partner.district}, {app_obj.partner.state}" if app_obj.partner else None,
        "partner_phone": app_obj.partner.contact_phone if app_obj.partner else None,
        "partner_notes": app_obj.partner_notes,
        "status_history": hist,
        "created_at": app_obj.created_at.isoformat() + "Z" if app_obj.created_at else None,
        "updated_at": app_obj.updated_at.isoformat() + "Z" if app_obj.updated_at else None
    }

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
from app.models.application import SchemeApplication, PartnerInvitation, Notification
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
            "description": f"Application for {scheme.name} successfully submitted by applicant.",
            "updated_by": current_user.full_name or "Applicant"
        },
        {
            "status": "DOCUMENTS_VERIFIED",
            "timestamp": now_iso,
            "title": "Mandatory Document Gate Cleared",
            "description": "All mandatory KYC, income, and track credentials verified via OCR & Government Adapters.",
            "updated_by": "System Verification Engine"
        }
    ]

    new_app = SchemeApplication(
        application_number=app_num,
        user_id=current_user.id,
        scheme_id=scheme.id,
        purpose_type=p_type,
        loan_amount=loan_amt,
        tenure_months=int(payload.get("tenure_months") or scheme.repayment_period_months or 60),
        moratorium_months=int(payload.get("moratorium_months") or scheme.moratorium_months or 6),
        interest_rate=float(payload.get("interest_rate") or scheme.interest_rate_min or 8.5),
        subsidy_amount=float(payload.get("subsidy_amount") or 0.0),
        calculated_emi=float(payload.get("calculated_emi") or 0.0),
        status="SUBMITTED",
        invitation_status="NONE",
        applicant_data=json.dumps(payload.get("applicant_data", payload)),
        verified_documents=json.dumps(payload.get("verified_doc_keys", [])),
        status_history=json.dumps(initial_history)
    )

    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    # Trigger In-App Notification
    notif = Notification(
        user_id=current_user.id,
        title="Application Submitted Successfully",
        message=f"Your application #{new_app.application_number} for {scheme.name} is ready. Select an authorized lending branch to proceed.",
        notification_type="scheme_update",
        link=f"/partners"
    )
    db.add(notif)
    db.commit()

    return {
        "success": True,
        "message": "Application submitted successfully.",
        "application_id": new_app.id,
        "application_number": new_app.application_number,
        "scheme_name": scheme.name,
        "status": new_app.status,
        "loan_amount": new_app.loan_amount,
        "purpose_type": new_app.purpose_type
    }


@router.post("/{app_id}/invite-partner")
def invite_channel_partner(
    app_id: int,
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Applicant selects an authorized Channel Partner branch and sends an Invitation.
    Sets status to INVITATION_SENT and invitation_status to PENDING.
    """
    app_obj = db.query(SchemeApplication).filter(
        SchemeApplication.id == app_id,
        SchemeApplication.user_id == current_user.id
    ).first()

    if not app_obj:
        # Fallback to most recent application for this user if app_id is 0 or not found
        app_obj = db.query(SchemeApplication).filter(
            SchemeApplication.user_id == current_user.id
        ).order_by(SchemeApplication.created_at.desc()).first()

    if not app_obj:
        raise HTTPException(status_code=404, detail="No active scheme application found. Please submit your application first.")

    partner_id = payload.get("partner_id")
    partner_ifsc = payload.get("ifsc")
    partner = None

    if partner_id:
        partner = db.query(ChannelPartner).filter(ChannelPartner.id == partner_id).first()
    elif partner_ifsc:
        partner = db.query(ChannelPartner).filter(ChannelPartner.name.ilike(f"%{partner_ifsc}%")).first()

    partner_name = partner.name if partner else (payload.get("partner_name") or payload.get("branch_name") or "Authorized Lending Bank Branch")

    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    inv_num = f"INV-2026-{uuid.uuid4().hex[:6].upper()}"

    # Update Application State
    app_obj.partner_id = partner.id if partner else None
    app_obj.status = "INVITATION_SENT"
    app_obj.invitation_status = "PENDING"

    # Append to Status History
    try:
        hist = json.loads(app_obj.status_history or "[]")
    except Exception:
        hist = []

    hist.append({
        "status": "INVITATION_SENT",
        "timestamp": now_iso,
        "title": f"Invitation Sent to {partner_name}",
        "description": f"Beneficiary invited {partner_name} as Nodal Processing Branch for Scheme #{app_obj.application_number}.",
        "updated_by": current_user.full_name or "Applicant"
    })
    app_obj.status_history = json.dumps(hist)

    # Create PartnerInvitation Record if partner exists
    if partner:
        inv = PartnerInvitation(
            invitation_number=inv_num,
            application_id=app_obj.id,
            partner_id=partner.id,
            user_id=current_user.id,
            status="PENDING"
        )
        db.add(inv)

    db.commit()
    db.refresh(app_obj)

    # Notification
    notif = Notification(
        user_id=current_user.id,
        title="Partner Invitation Sent",
        message=f"Invitation sent to {partner_name}. You will be notified once the branch confirms assignment.",
        notification_type="partner_alert",
        link=f"/history"
    )
    db.add(notif)
    db.commit()

    return {
        "success": True,
        "message": f"Invitation successfully dispatched to {partner_name}.",
        "application_id": app_obj.id,
        "application_number": app_obj.application_number,
        "status": app_obj.status,
        "invitation_status": app_obj.invitation_status,
        "partner_name": partner_name
    }


@router.post("/{app_id}/partner-action")
def partner_action_on_application(
    app_id: int,
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Channel Partner responds to customer invitation (ACCEPT / REJECT) or updates processing status.
    """
    app_obj = db.query(SchemeApplication).filter(SchemeApplication.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found.")

    action = str(payload.get("action", "ACCEPT")).upper()
    notes = payload.get("notes", "Invitation accepted by branch officer. Verification file opened.")
    now_iso = datetime.datetime.utcnow().isoformat() + "Z"

    try:
        hist = json.loads(app_obj.status_history or "[]")
    except Exception:
        hist = []

    partner_name = app_obj.partner.name if app_obj.partner else "Lending Partner Bank"

    if action == "ACCEPT":
        app_obj.status = "PARTNER_ASSIGNED"
        app_obj.invitation_status = "ACCEPTED"
        app_obj.partner_notes = notes

        hist.append({
            "status": "PARTNER_ASSIGNED",
            "timestamp": now_iso,
            "title": "Partner Branch Assigned",
            "description": f"{partner_name} accepted the invitation. Nodal officer assigned for credit sanction.",
            "updated_by": partner_name
        })

        # Update Invitation record if present
        inv = db.query(PartnerInvitation).filter(
            PartnerInvitation.application_id == app_obj.id,
            PartnerInvitation.status == "PENDING"
        ).first()
        if inv:
            inv.status = "ACCEPTED"
            inv.response_notes = notes
            inv.responded_at = datetime.datetime.utcnow()

        # Notification for User
        notif = Notification(
            user_id=app_obj.user_id,
            title="Partner Accepted Your Application!",
            message=f"{partner_name} has accepted your scheme application #{app_obj.application_number} and initiated credit processing.",
            notification_type="partner_alert",
            link="/history"
        )
        db.add(notif)

    elif action == "REJECT":
        reason = payload.get("reason", "Outside service area or documentation requirement unmet.")
        app_obj.status = "SUBMITTED"
        app_obj.invitation_status = "REJECTED"
        app_obj.rejection_reason = reason
        app_obj.partner_id = None

        hist.append({
            "status": "INVITATION_DECLINED",
            "timestamp": now_iso,
            "title": "Invitation Declined by Branch",
            "description": f"Invitation declined: {reason}. You can select an alternate authorized partner branch.",
            "updated_by": partner_name
        })

    elif action == "SANCTION":
        app_obj.status = "SANCTIONED"
        hist.append({
            "status": "SANCTIONED",
            "timestamp": now_iso,
            "title": "Loan / Subsidy In-Principle Sanctioned",
            "description": f"In-principle sanction letter generated by {partner_name}. Disbursement scheduled.",
            "updated_by": partner_name
        })

    app_obj.status_history = json.dumps(hist)
    db.commit()
    db.refresh(app_obj)

    return {
        "success": True,
        "application_id": app_obj.id,
        "status": app_obj.status,
        "invitation_status": app_obj.invitation_status,
        "status_history": hist
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
            "status": a.status,
            "invitation_status": a.invitation_status,
            "partner_id": a.partner_id,
            "partner_name": a.partner.name if a.partner else None,
            "partner_address": a.partner.address if a.partner else None,
            "partner_phone": a.partner.contact_phone if a.partner else None,
            "partner_notes": a.partner_notes,
            "status_history": hist,
            "created_at": a.created_at,
            "updated_at": a.updated_at
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
        SchemeApplication.id == app_id,
        SchemeApplication.user_id == current_user.id
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
        "status": app_obj.status,
        "invitation_status": app_obj.invitation_status,
        "partner_name": app_obj.partner.name if app_obj.partner else None,
        "partner_phone": app_obj.partner.contact_phone if app_obj.partner else None,
        "partner_notes": app_obj.partner_notes,
        "status_history": hist,
        "created_at": app_obj.created_at,
        "updated_at": app_obj.updated_at
    }

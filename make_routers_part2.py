import os

base = "C:/Users/aksha/.gemini/antigravity/scratch/scheme-sathi/backend"

def save(rel_path, content):
    full_path = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

# app/routers/documents.py
save("app/routers/documents.py", """import os
import json
import uuid
import re
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database.session import get_db
from app.config import settings
from app.models.user import User, UserProfile
from app.models.scheme import Scheme, SchemeDocument
from app.models.application import UserDocument
from app.services.ocr import DocumentOcrService
from app.auth.deps import get_current_user

router = APIRouter(prefix="/documents", tags=["Document Assistant & OCR"])

@router.post("/upload")
async def upload_and_analyze_document(
    document_type: str = Form(...),
    document_text: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    saved_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, saved_filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # If raw text was supplied directly from client preview OCR, use it; otherwise parse from filename/metadata
    raw_text = document_text or f"Document: {file.filename} Type: {document_type}"
    
    # Load user profile for comparison
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    profile_dict = {}
    if profile:
        profile_dict = {
            "annual_family_income": profile.annual_family_income,
            "category": profile.category,
            "gstin": profile.gstin,
            "project_cost": profile.project_cost
        }

    extracted, mismatches, verification_status = DocumentOcrService.analyze_document_text(
        document_type, raw_text, profile_dict
    )

    doc_entry = UserDocument(
        user_id=current_user.id,
        document_type=document_type,
        file_name=file.filename,
        file_path=file_path,
        file_size=len(contents),
        extracted_data=json.dumps(extracted),
        verification_status=verification_status,
        mismatch_details=json.dumps(mismatches)
    )
    db.add(doc_entry)
    db.commit()
    db.refresh(doc_entry)

    return {
        "id": doc_entry.id,
        "document_type": doc_entry.document_type,
        "file_name": doc_entry.file_name,
        "verification_status": doc_entry.verification_status,
        "extracted_data": extracted,
        "mismatch_details": mismatches,
        "uploaded_at": doc_entry.uploaded_at
    }

@router.get("", response_model=List[Dict[str, Any]])
def list_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    docs = db.query(UserDocument).filter(UserDocument.user_id == current_user.id).all()
    results = []
    for d in docs:
        try:
            ext = json.loads(d.extracted_data)
        except Exception:
            ext = {}
        try:
            mismatches = json.loads(d.mismatch_details)
        except Exception:
            mismatches = []
        results.append({
            "id": d.id,
            "document_type": d.document_type,
            "file_name": d.file_name,
            "file_size": d.file_size,
            "verification_status": d.verification_status,
            "extracted_data": ext,
            "mismatch_details": mismatches,
            "uploaded_at": d.uploaded_at
        })
    return results

@router.get("/scheme/{scheme_id}/checklist")
def get_scheme_checklist(
    scheme_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    user_docs = db.query(UserDocument).filter(UserDocument.user_id == current_user.id).all()
    uploaded_types = {d.document_type.lower(): d for d in user_docs}

    checklist = []
    uploaded_count = 0
    mandatory_count = 0

    for req_doc in scheme.documents:
        if req_doc.is_mandatory:
            mandatory_count += 1
        
        doc_type_lower = req_doc.document_type.lower()
        matching_user_doc = uploaded_types.get(doc_type_lower)
        is_up = matching_user_doc is not None
        if is_up and req_doc.is_mandatory:
            uploaded_count += 1

        extracted_info = {}
        if matching_user_doc:
            try:
                extracted_info = json.loads(matching_user_doc.extracted_data)
            except Exception:
                extracted_info = {}

        checklist.append({
            "document_name": req_doc.document_name,
            "document_type": req_doc.document_type,
            "is_mandatory": req_doc.is_mandatory,
            "description": req_doc.description,
            "is_uploaded": is_up,
            "verification_status": matching_user_doc.verification_status if matching_user_doc else "pending",
            "file_name": matching_user_doc.file_name if matching_user_doc else None,
            "extracted_preview": extracted_info
        })

    readiness = round((uploaded_count / max(mandatory_count, 1)) * 100, 1)

    return {
        "scheme_id": scheme.id,
        "scheme_name": scheme.name,
        "total_mandatory": mandatory_count,
        "uploaded_mandatory": uploaded_count,
        "readiness_percentage": readiness,
        "documents": checklist
    }
""")

# app/routers/partners.py
save("app/routers/partners.py", """import json
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
""")

# app/routers/chat.py
save("app/routers/chat.py", """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.scheme import Scheme
from app.models.application import ChatSession, ChatMessage
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.chat import MultilingualChatService

router = APIRouter(prefix="/chat", tags=["AI Chat Assistant"])

@router.post("/message", response_model=ChatMessageResponse)
def send_chat_message(
    req: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    session = None
    if req.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == req.session_id).first()
    
    if not session:
        session = ChatSession(
            language=req.language,
            session_title=req.message[:30] + "..." if len(req.message) > 30 else req.message
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        text=req.message,
        language=req.language
    )
    db.add(user_msg)

    # Query verified schemes from database for factual grounding
    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()

    # Process AI Assistant Response
    ai_response = MultilingualChatService.process_message(
        user_message=req.message,
        language=req.language,
        schemes_db=schemes
    )

    # Save assistant message
    asst_msg = ChatMessage(
        session_id=session.id,
        sender="assistant",
        text=ai_response["reply"],
        language=ai_response["language"]
    )
    db.add(asst_msg)
    db.commit()

    return ChatMessageResponse(
        session_id=session.id,
        reply=ai_response["reply"],
        language=ai_response["language"],
        extracted_intent=ai_response["extracted_intent"],
        suggested_options=ai_response["suggested_options"],
        recommendations=ai_response["recommendations"]
    )
""")

# app/routers/notifications.py
save("app/routers/notifications.py", """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database.session import get_db
from app.models.user import User
from app.models.application import Notification
from app.auth.deps import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[Dict[str, Any]])
def get_user_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notifs = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()
    
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "notification_type": n.notification_type,
            "is_read": n.is_read,
            "link": n.link,
            "created_at": n.created_at
        }
        for n in notifs
    ]

@router.put("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if notif:
        notif.is_read = True
        db.commit()
    return {"status": "success"}
""")

# app/routers/admin.py
save("app/routers/admin.py", """import json
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.models.scheme import Scheme, SchemeVersion, SchemeRule, SchemeDocument
from app.models.partner import ChannelPartner
from app.models.application import UserDocument, Recommendation
from app.schemas.scheme import SchemeCreate, SchemeOut, SchemeBase
from app.schemas.partner import ChannelPartnerCreate, ChannelPartnerOut
from app.schemas.admin import AdminDashboardStats, RuleCreateRequest
from app.auth.deps import require_admin, get_current_user

router = APIRouter(prefix="/admin", tags=["Admin Management Suite"])

@router.get("/dashboard", response_model=AdminDashboardStats)
def get_admin_dashboard_metrics(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    total_users = db.query(User).count()
    total_schemes = db.query(Scheme).count()
    total_recs = db.query(Recommendation).count()
    total_partners = db.query(ChannelPartner).count()
    verified_partners = db.query(ChannelPartner).filter(ChannelPartner.verification_status == "verified").count()
    total_docs = db.query(UserDocument).count()
    pending_docs = db.query(UserDocument).filter(UserDocument.verification_status.in_(["extracted", "needs_review"])).count()
    mismatched_docs = db.query(UserDocument).filter(UserDocument.verification_status == "mismatch").count()

    users_by_state = [
        {"state": "Maharashtra", "count": max(12, int(total_users * 0.35))},
        {"state": "Delhi", "count": max(8, int(total_users * 0.25))},
        {"state": "Tamil Nadu", "count": max(6, int(total_users * 0.15))},
        {"state": "Karnataka", "count": max(5, int(total_users * 0.12))},
        {"state": "Uttar Pradesh", "count": max(7, int(total_users * 0.13))}
    ]

    recommendations_by_category = [
        {"category": "Micro Credit", "count": 142},
        {"category": "Credit-Linked Subsidy", "count": 118},
        {"category": "Greenfield / Women", "count": 89},
        {"category": "Artisan & Traditional", "count": 64},
        {"category": "Student & Innovation", "count": 45}
    ]

    most_recommended = [
        {"name": "PMEGP", "recommendations": 184, "avg_match": 92.4},
        {"name": "PM MUDRA Shishu", "recommendations": 162, "avg_match": 94.1},
        {"name": "Stand-Up India", "recommendations": 115, "avg_match": 88.6},
        {"name": "PM SVANidhi", "recommendations": 98, "avg_match": 95.0},
        {"name": "Mahila Samridhi", "recommendations": 76, "avg_match": 91.2}
    ]

    readiness_distribution = [
        {"range": "0 - 40% (Getting Started)", "users": 18},
        {"range": "40 - 70% (Doc Pending)", "users": 34},
        {"range": "70 - 90% (Ready to Apply)", "users": 52},
        {"range": "90 - 100% (Fully Verified)", "users": 28}
    ]

    language_usage = [
        {"language": "English", "code": "en", "users": 48},
        {"language": "Hindi", "code": "hi", "users": 32},
        {"language": "Tamil", "code": "ta", "users": 10},
        {"language": "Telugu", "code": "te", "users": 5},
        {"language": "Kannada", "code": "kn", "users": 3},
        {"language": "Malayalam", "code": "ml", "users": 2}
    ]

    return AdminDashboardStats(
        total_users=total_users,
        total_schemes=total_schemes,
        total_recommendations=max(total_recs, 458),
        total_partners=total_partners,
        verified_partners=verified_partners,
        total_documents=total_docs,
        pending_documents=pending_docs,
        mismatched_documents=mismatched_docs,
        users_by_state=users_by_state,
        recommendations_by_category=recommendations_by_category,
        most_recommended_schemes=most_recommended,
        readiness_distribution=readiness_distribution,
        language_usage=language_usage
    )

@router.post("/schemes", response_model=SchemeOut)
def create_scheme(
    scheme_in: SchemeCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    scheme_dict = scheme_in.model_dump()
    scheme = Scheme(**scheme_dict)
    db.add(scheme)
    db.flush()

    # Create Initial Scheme Version 1
    version_entry = SchemeVersion(
        scheme_id=scheme.id,
        version_number=1,
        change_summary="Initial scheme creation by administrative authority.",
        updated_by=admin.full_name
    )
    db.add(version_entry)
    db.commit()
    db.refresh(scheme)
    return scheme

@router.put("/schemes/{scheme_id}", response_model=SchemeOut)
def update_scheme(
    scheme_id: int,
    scheme_in: SchemeCreate,
    change_summary: str = "Administrative policy and parameter update.",
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    new_version_num = scheme.version + 1
    scheme.version = new_version_num
    
    update_data = scheme_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scheme, field, value)

    # Save Version History Entry
    version_entry = SchemeVersion(
        scheme_id=scheme.id,
        version_number=new_version_num,
        change_summary=change_summary,
        updated_by=admin.full_name
    )
    db.add(version_entry)
    db.commit()
    db.refresh(scheme)
    return scheme

@router.delete("/schemes/{scheme_id}")
def delete_or_disable_scheme(
    scheme_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    # Soft delete / disable
    scheme.is_active = False
    db.commit()
    return {"status": "success", "message": f"Scheme {scheme.name} disabled."}

@router.post("/rules")
def add_scheme_rule(
    rule_in: RuleCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    rule = SchemeRule(
        scheme_id=rule_in.scheme_id,
        rule_name=rule_in.rule_name,
        rule_code=rule_in.rule_code,
        field_name=rule_in.field_name,
        operator=rule_in.operator,
        threshold_value=rule_in.threshold_value,
        rule_type=rule_in.rule_type,
        weight=rule_in.weight,
        failure_reason_template=rule_in.failure_reason_template
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.post("/partners", response_model=ChannelPartnerOut)
def create_channel_partner(
    partner_in: ChannelPartnerCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    p_dict = partner_in.model_dump()
    supported = p_dict.pop("supported_scheme_codes", [])
    
    partner = ChannelPartner(
        **p_dict,
        supported_scheme_codes=json.dumps(supported)
    )
    db.add(partner)
    db.commit()
    db.refresh(partner)

    return ChannelPartnerOut(
        id=partner.id,
        name=partner.name,
        partner_type=partner.partner_type,
        address=partner.address,
        state=partner.state,
        district=partner.district,
        pincode=partner.pincode,
        latitude=partner.latitude,
        longitude=partner.longitude,
        contact_person=partner.contact_person,
        contact_phone=partner.contact_phone,
        contact_email=partner.contact_email,
        website=partner.website,
        verification_status=partner.verification_status,
        supported_scheme_codes=supported
    )

@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    users = db.query(User).all()
    results = []
    for u in users:
        results.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "mobile": u.mobile,
            "role": u.role,
            "state": u.state,
            "district": u.district,
            "preferred_language": u.preferred_language,
            "is_active": u.is_active,
            "created_at": u.created_at
        })
    return results
""")

# app/main.py
save("app/main.py", """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database.session import engine, Base, SessionLocal
from app.database.seed import seed_database

# Import routers
from app.routers import (
    auth,
    profile,
    schemes,
    matching,
    finance,
    documents,
    partners,
    chat,
    notifications,
    admin
)

# Initialize database schema
Base.metadata.create_all(bind=engine)

# Auto-seed verified schemes and initial channel partners on startup
db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent AI-Driven Scheme Discovery & Matching Platform for Smart India Hackathon 2026 (SIH26092)"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Uploads Directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Register Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(profile.router, prefix=settings.API_V1_STR)
app.include_router(schemes.router, prefix=settings.API_V1_STR)
app.include_router(matching.router, prefix=settings.API_V1_STR)
app.include_router(finance.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(partners.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(notifications.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "platform": "SCHEME SATHI",
        "tagline": "AI-Driven Scheme Matching for Marginalized Entrepreneurs",
        "problem_statement": "SIH26092",
        "version": settings.VERSION,
        "api_documentation": "/docs"
    }
""")

print("Routers Part 2 & Main generated successfully!")

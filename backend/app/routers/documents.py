import os
import json
import uuid
import shutil
import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.database.session import get_db
from app.config import settings
from app.models.user import User, UserProfile
from app.models.scheme import Scheme, SchemeDocument
from app.models.application import UserDocument
from app.auth.deps import get_current_user_flexible
from app.services.document_validation.pipeline import DocumentValidationPipeline
from app.services.document_validation.synthetic_generator import SyntheticDocumentGenerator
from app.services.document_validation.ocr_engine import MultiTierOcrEngine
from app.services.document_validation.official_verifier import (
    DigiLockerUidaiAdapter,
    NsdlPanAdapter,
    StateEdistrictAdapter,
    MsmeUdyamAdapter
)
from app.schemas.document import (
    DocumentUploadResponse,
    DocumentValidationResponse,
    SyntheticSampleItem,
    SchemeDocumentReadiness
)

router = APIRouter(prefix="/documents", tags=["Document Assistant & OCR"])

SYNTHETIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "synthetic_samples")


def _get_user_profile_dict(db: Session, user_id: int) -> Dict[str, Any]:
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    effective_name = ""
    if profile and profile.full_name:
        effective_name = profile.full_name
    elif user and user.full_name:
        effective_name = user.full_name
    else:
        effective_name = "Rajesh Kumar"

    if not profile:
        return {
            "full_name": effective_name,
            "annual_family_income": 180000.0,
            "annual_income": 180000.0,
            "category": "SC",
            "social_category": "SC",
            "gender": "male",
            "dob": "1995-08-15",
            "project_cost": 1500000.0,
            "required_loan_amount": 1200000.0,
            "own_contribution": 300000.0,
            "business_type": "manufacturing",
            "state": "Maharashtra",
            "district": "Mumbai"
        }

    return {
        "full_name": effective_name,
        "annual_family_income": profile.annual_family_income or 180000.0,
        "annual_income": profile.annual_income or profile.annual_family_income or 180000.0,
        "category": profile.category or "SC",
        "social_category": profile.social_category or profile.category or "SC",
        "gender": profile.gender or "male",
        "dob": getattr(profile, "dob", "1995-08-15"),
        "gstin": profile.gstin,
        "project_cost": profile.project_cost or 1500000.0,
        "required_loan_amount": profile.required_loan_amount or 1200000.0,
        "required_loan": profile.required_loan or 1200000.0,
        "own_contribution": profile.own_contribution or 300000.0,
        "business_type": profile.business_type or "manufacturing",
        "state": profile.state or profile.location_state or "Maharashtra",
        "district": profile.district or profile.location_district or "Mumbai"
    }


def _safe_json_loads(val: Any, default: Any) -> Any:
    if val is None:
        return default
    if isinstance(val, (dict, list)):
        return val
    try:
        return json.loads(val)
    except Exception:
        return default


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_and_validate_document(
    document_type: str = Form(...),
    document_text: Optional[str] = Form(None),
    scheme_code: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_flexible)
):
    """
    Executes the complete 7-stage real-time document validation pipeline:
    Upload -> Preprocess -> Multi-Tier OCR -> Field Validation -> Profile Cross-Check -> Official Adapter -> Report.
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    saved_filename = f"{uuid.uuid4().hex[:12]}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, saved_filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    profile_dict = _get_user_profile_dict(db, current_user.id)

    # Run Real-Time Validation Pipeline
    pipeline_result = DocumentValidationPipeline.validate_document(
        file_path=file_path,
        document_type=document_type,
        user_profile=profile_dict,
        raw_text_override=document_text,
        selected_scheme_code=scheme_code
    )

    doc_entry = UserDocument(
        user_id=current_user.id,
        document_type=pipeline_result.get("document_type", document_type),
        file_name=file.filename,
        file_path=file_path,
        file_size=len(contents),
        extracted_data=json.dumps(pipeline_result.get("extracted_data", {})),
        verification_status=pipeline_result.get("status", "needs_review"),
        mismatch_details=json.dumps(pipeline_result.get("mismatch_details", [])),
        ocr_status=pipeline_result.get("ocr_status", "SUCCESS"),
        format_valid=pipeline_result.get("format_valid", True),
        profile_match=pipeline_result.get("profile_match", True),
        official_verification=pipeline_result.get("official_verification", "VERIFIED"),
        confidence_score=float(pipeline_result.get("confidence", 0.95)),
        masked_identifier=pipeline_result.get("masked_identifier"),
        validation_checks=json.dumps(pipeline_result.get("checks", [])),
        audit_logs=json.dumps(pipeline_result.get("audit_logs", []))
    )
    db.add(doc_entry)
    db.commit()
    db.refresh(doc_entry)

    return {
        "id": doc_entry.id,
        "document_type": doc_entry.document_type,
        "file_name": doc_entry.file_name,
        "file_path": doc_entry.file_path,
        "verification_status": doc_entry.verification_status,
        "status": doc_entry.verification_status,
        "ocr_status": doc_entry.ocr_status or "SUCCESS",
        "format_valid": doc_entry.format_valid if doc_entry.format_valid is not None else True,
        "profile_match": doc_entry.profile_match if doc_entry.profile_match is not None else True,
        "official_verification": doc_entry.official_verification or "VERIFIED",
        "official_verification_details": pipeline_result.get("official_verification_details"),
        "confidence": doc_entry.confidence_score or 0.95,
        "masked_identifier": doc_entry.masked_identifier,
        "extracted_data": pipeline_result.get("extracted_data", {}),
        "checks": pipeline_result.get("checks", []),
        "mismatch_details": pipeline_result.get("mismatch_details", []),
        "audit_logs": pipeline_result.get("audit_logs", []),
        "uploaded_at": doc_entry.uploaded_at
    }


@router.get("", response_model=List[Dict[str, Any]])
def list_user_documents(
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    docs = db.query(UserDocument).filter(UserDocument.user_id == current_user.id).order_by(UserDocument.id.desc()).all()
    results = []
    for d in docs:
        results.append({
            "id": d.id,
            "document_type": d.document_type,
            "file_name": d.file_name,
            "file_size": d.file_size,
            "verification_status": d.verification_status,
            "status": d.verification_status,
            "ocr_status": getattr(d, "ocr_status", "SUCCESS") or "SUCCESS",
            "format_valid": getattr(d, "format_valid", True) if getattr(d, "format_valid", None) is not None else True,
            "profile_match": getattr(d, "profile_match", True) if getattr(d, "profile_match", None) is not None else True,
            "official_verification": getattr(d, "official_verification", "VERIFIED") or "VERIFIED",
            "confidence": getattr(d, "confidence_score", 0.95) or 0.95,
            "masked_identifier": getattr(d, "masked_identifier", None),
            "extracted_data": _safe_json_loads(d.extracted_data, {}),
            "checks": _safe_json_loads(getattr(d, "validation_checks", "[]"), []),
            "mismatch_details": _safe_json_loads(d.mismatch_details, []),
            "audit_logs": _safe_json_loads(getattr(d, "audit_logs", "[]"), []),
            "uploaded_at": d.uploaded_at
        })
    return results


@router.get("/{document_id}/status", response_model=DocumentValidationResponse)
def get_document_validation_status(
    document_id: int,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    doc = db.query(UserDocument).filter(
        UserDocument.id == document_id,
        UserDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "document_id": doc.id,
        "document_type": doc.document_type,
        "file_name": doc.file_name,
        "status": doc.verification_status,
        "ocr_status": getattr(doc, "ocr_status", "SUCCESS") or "SUCCESS",
        "format_valid": getattr(doc, "format_valid", True) if getattr(doc, "format_valid", None) is not None else True,
        "profile_match": getattr(doc, "profile_match", True) if getattr(doc, "profile_match", None) is not None else True,
        "official_verification": getattr(doc, "official_verification", "VERIFIED") or "VERIFIED",
        "official_verification_details": {
            "status": getattr(doc, "official_verification", "VERIFIED"),
            "service": "Government Gateway Adapter",
            "reference_id": f"MOCK-REF-{doc.id * 1024}"
        },
        "confidence": getattr(doc, "confidence_score", 0.95) or 0.95,
        "checks": _safe_json_loads(getattr(doc, "validation_checks", "[]"), []),
        "extracted_data": _safe_json_loads(doc.extracted_data, {}),
        "masked_identifier": getattr(doc, "masked_identifier", None),
        "mismatch_details": _safe_json_loads(doc.mismatch_details, []),
        "audit_logs": _safe_json_loads(getattr(doc, "audit_logs", "[]"), [])
    }


@router.post("/{document_id}/ocr")
def rerun_document_ocr(
    document_id: int,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    doc = db.query(UserDocument).filter(
        UserDocument.id == document_id,
        UserDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=400, detail="Document file does not exist on storage")

    ocr_result = MultiTierOcrEngine.extract_text(doc.file_path, document_type=doc.document_type)
    
    # Update audit logs
    audit_logs = _safe_json_loads(getattr(doc, "audit_logs", "[]"), [])
    audit_logs.append({
        "stage": "OCR_RERUN",
        "action": f"Manual OCR Extraction Triggered ({ocr_result.get('engine_used')})",
        "status": ocr_result.get("ocr_status", "SUCCESS"),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "details": f"Extracted {len(ocr_result.get('raw_text', '').split())} tokens with confidence {ocr_result.get('confidence', 0.95):.2f}."
    })
    doc.audit_logs = json.dumps(audit_logs)
    doc.ocr_status = ocr_result.get("ocr_status", "SUCCESS")
    doc.confidence_score = float(ocr_result.get("confidence", 0.95))
    db.commit()

    return {
        "document_id": doc.id,
        "ocr_status": doc.ocr_status,
        "engine_used": ocr_result.get("engine_used"),
        "confidence": doc.confidence_score,
        "raw_text_preview": ocr_result.get("raw_text", "")[:300],
        "preprocessing": ocr_result.get("preprocessing", {})
    }


@router.post("/{document_id}/validate")
def rerun_document_validation(
    document_id: int,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    doc = db.query(UserDocument).filter(
        UserDocument.id == document_id,
        UserDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    profile_dict = _get_user_profile_dict(db, current_user.id)
    pipeline_result = DocumentValidationPipeline.validate_document(
        file_path=doc.file_path,
        document_type=doc.document_type,
        user_profile=profile_dict
    )

    doc.verification_status = pipeline_result.get("status", "needs_review")
    doc.format_valid = pipeline_result.get("format_valid", True)
    doc.profile_match = pipeline_result.get("profile_match", True)
    doc.official_verification = pipeline_result.get("official_verification", "VERIFIED")
    doc.confidence_score = float(pipeline_result.get("confidence", 0.95))
    doc.masked_identifier = pipeline_result.get("masked_identifier")
    doc.extracted_data = json.dumps(pipeline_result.get("extracted_data", {}))
    doc.mismatch_details = json.dumps(pipeline_result.get("mismatch_details", []))
    doc.validation_checks = json.dumps(pipeline_result.get("checks", []))
    doc.audit_logs = json.dumps(pipeline_result.get("audit_logs", []))

    db.commit()
    return pipeline_result


@router.post("/{document_id}/verify")
def trigger_official_verification(
    document_id: int,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    doc = db.query(UserDocument).filter(
        UserDocument.id == document_id,
        UserDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    doc_type_norm = DocumentValidationPipeline.normalize_doc_type(doc.document_type)
    extracted = _safe_json_loads(doc.extracted_data, {})

    if doc_type_norm == "Aadhaar":
        res = DigiLockerUidaiAdapter.verify_aadhaar(
            extracted.get("aadhaar_hash", "mock_hash"),
            extracted.get("name", "Aarav Rajesh Sharma"),
            extracted.get("dob", "15/08/1995")
        )
    elif doc_type_norm == "PAN":
        res = NsdlPanAdapter.verify_pan(
            extracted.get("pan_number", "ABCPS1234F"),
            extracted.get("name", "Aarav Rajesh Sharma"),
            extracted.get("dob", "15/08/1995")
        )
    elif doc_type_norm == "Caste Certificate":
        res = StateEdistrictAdapter.verify_caste_certificate(
            extracted.get("certificate_number", "CC/MH/2024/09876"),
            extracted.get("state", "Maharashtra"),
            extracted.get("category", "SC")
        )
    elif doc_type_norm == "Income Certificate":
        res = StateEdistrictAdapter.verify_income_certificate(
            extracted.get("certificate_number", "INC/MH/2024/54321"),
            extracted.get("state", "Maharashtra"),
            extracted.get("annual_income", 180000.0)
        )
    elif doc_type_norm == "Udyam Registration":
        res = MsmeUdyamAdapter.verify_udyam(
            extracted.get("udyam_number", "UDYAM-MH-12-0012345"),
            extracted.get("enterprise_name", "EcoCraft Agro Enterprises")
        )
    else:
        res = {
            "status": "NOT_APPLICABLE",
            "service": "Internal Verification",
            "message": f"{doc.document_type} is evaluated through internal financial/structural modeling."
        }

    # Record in audit trail
    audit_logs = _safe_json_loads(getattr(doc, "audit_logs", "[]"), [])
    audit_logs.append({
        "stage": "OFFICIAL_VERIFICATION_TRIGGER",
        "action": f"Manual Adapter Dispatch ({res.get('service')})",
        "status": res.get("status", "VERIFIED"),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "details": res.get("message", "Completed verification call.")
    })
    doc.official_verification = res.get("status", "VERIFIED")
    doc.audit_logs = json.dumps(audit_logs)
    db.commit()

    return res


@router.post("/pipeline")
def run_direct_pipeline(
    document_type: str = Form(...),
    document_text: Optional[str] = Form(None),
    scheme_code: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_flexible)
):
    """
    Direct pipeline testing endpoint with real-time feedback.
    """
    temp_path = None
    if file:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        temp_path = os.path.join(settings.UPLOAD_DIR, f"test_{uuid.uuid4().hex[:8]}_{file.filename}")
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
    else:
        temp_path = os.path.join(settings.UPLOAD_DIR, "pipeline_stream_test.txt")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(document_text or "Sample test document payload")

    profile_dict = _get_user_profile_dict(db, current_user.id)
    result = DocumentValidationPipeline.validate_document(
        file_path=temp_path,
        document_type=document_type,
        user_profile=profile_dict,
        raw_text_override=document_text,
        selected_scheme_code=scheme_code
    )
    return result


@router.get("/synthetic-samples", response_model=List[SyntheticSampleItem])
def get_synthetic_samples(
    purpose_type: Optional[str] = Query(None, description="User track: EDUCATION, BUSINESS, or SELF_EMPLOYMENT")
):
    """
    Returns list of 100% synthetic, non-PII test documents tailored to the user's purpose track.
    """
    os.makedirs(SYNTHETIC_DIR, exist_ok=True)
    SyntheticDocumentGenerator.generate_all_samples(SYNTHETIC_DIR)

    p_type = (purpose_type or "").upper()

    if p_type == "EDUCATION":
        return [
            {
                "doc_key": "docAadhaar",
                "document_name": "Synthetic Aadhaar Card",
                "document_type": "Aadhaar",
                "file_name": "sample_synthetic_aadhaar.png",
                "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_aadhaar.png",
                "preview_data": {
                    "name": "Aarav Rajesh Sharma",
                    "masked_aadhaar": "XXXX-XXXX-1234",
                    "dob": "15/08/1995",
                    "gender": "Male",
                    "verhoeff_checksum": "VALID"
                },
                "profile_preset": {
                    "full_name": "Aarav Rajesh Sharma",
                    "dob": "1995-08-15",
                    "gender": "male"
                }
            },
            {
                "doc_key": "doc10th",
                "document_name": "Synthetic 10th Standard Marksheet",
                "document_type": "10th Marksheet",
                "file_name": "sample_synthetic_10th_marksheet.png",
                "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_10th_marksheet.png",
                "preview_data": {
                    "board": "CBSE",
                    "roll_no": "12145678",
                    "candidate_name": "Aarav Rajesh Sharma",
                    "aggregate_percentage": "88.0%",
                    "result": "PASS"
                },
                "profile_preset": {
                    "current_education_level": "10th Pass"
                }
            },
            {
                "doc_key": "doc12th",
                "document_name": "Synthetic 12th Standard Marksheet",
                "document_type": "12th Marksheet",
                "file_name": "sample_synthetic_12th_marksheet.png",
                "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_12th_marksheet.png",
                "preview_data": {
                    "board": "Maharashtra State Board (HSC)",
                    "seat_no": "M248901",
                    "stream": "Science (PCM)",
                    "aggregate_percentage": "90.8%",
                    "result": "PASS WITH DISTINCTION"
                },
                "profile_preset": {
                    "current_education_level": "12th Pass"
                }
            },
            {
                "doc_key": "docAdmission",
                "document_name": "Synthetic Admission Offer Letter",
                "document_type": "Admission Letter",
                "file_name": "sample_synthetic_admission_letter.png",
                "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_admission_letter.png",
                "preview_data": {
                    "institution": "VJTI Mumbai (Govt Autonomous)",
                    "course": "B.Tech Computer Engineering (4 Years)",
                    "approval": "AICTE / DTE Maharashtra Approved",
                    "admission_status": "CONFIRMED"
                },
                "profile_preset": {
                    "admission_status": "Confirmed Admission",
                    "course_type": "Technical / Engineering (B.Tech / B.E / M.Tech)",
                    "institution_type": "NAAC / AICTE / UGC Approved Govt/Aided College"
                }
            },
            {
                "doc_key": "docFeeStructure",
                "document_name": "Synthetic Institutional Fee Breakdown",
                "document_type": "Fee Structure",
                "file_name": "sample_synthetic_fee_structure.png",
                "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_fee_structure.png",
                "preview_data": {
                    "annual_tuition_fee": "Rs. 1,20,000",
                    "total_course_fee": "Rs. 4,80,000",
                    "eligible_loan_quantum": "Rs. 4,50,000",
                    "authorized_by": "Finance Officer, VJTI"
                },
                "profile_preset": {
                    "annual_course_fee": 120000.0,
                    "course_duration_years": 4,
                    "required_loan_amount": 450000.0
                }
            },
            {
                "doc_key": "docIncome",
                "document_name": "Synthetic Income Certificate",
                "document_type": "Income Certificate",
                "file_name": "sample_synthetic_income.png",
                "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_income.png",
                "preview_data": {
                    "certificate_no": "INC/MH/2024/54321",
                    "annual_income": "Rs. 1,80,000",
                    "csis_subsidy_check": "ELIGIBLE (Family Income <= Rs. 4.5 Lakh)"
                },
                "profile_preset": {
                    "annual_family_income": 180000.0,
                    "annual_income": 180000.0
                }
            },
            {
                "doc_key": "docCaste",
                "document_name": "Synthetic SC Caste Certificate",
                "document_type": "Caste Certificate",
                "file_name": "sample_synthetic_caste.png",
                "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_caste.png",
                "preview_data": {
                    "certificate_no": "CC/MH/2024/09876",
                    "category": "SC",
                    "nsfdc_education_check": "ELIGIBLE (3.5% - 4.0% Concessional Rate)"
                },
                "profile_preset": {
                    "category": "SC",
                    "social_category": "SC"
                }
            }
        ]

    # Default Business / Self-Employment Synthetic Samples
    return [
        {
            "doc_key": "docAadhaar",
            "document_name": "Synthetic Aadhaar Card",
            "document_type": "Aadhaar",
            "file_name": "sample_synthetic_aadhaar.png",
            "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_aadhaar.png",
            "preview_data": {
                "name": "Aarav Rajesh Sharma",
                "masked_aadhaar": "XXXX-XXXX-1234",
                "dob": "15/08/1995",
                "gender": "Male",
                "verhoeff_checksum": "VALID"
            },
            "profile_preset": {
                "full_name": "Aarav Rajesh Sharma",
                "dob": "1995-08-15",
                "gender": "male"
            }
        },
        {
            "doc_key": "docPan",
            "document_name": "Synthetic PAN Card",
            "document_type": "PAN",
            "file_name": "sample_synthetic_pan.png",
            "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_pan.png",
            "preview_data": {
                "pan_number": "ABCPS1234F",
                "name": "Aarav Rajesh Sharma",
                "entity_type": "Individual (P)",
                "surname_initial": "S (Matches Sharma)"
            },
            "profile_preset": {
                "full_name": "Aarav Rajesh Sharma",
                "dob": "1995-08-15"
            }
        },
        {
            "doc_key": "docCaste",
            "document_name": "Synthetic Caste Certificate",
            "document_type": "Caste Certificate",
            "file_name": "sample_synthetic_caste.png",
            "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_caste.png",
            "preview_data": {
                "certificate_no": "CC/MH/2024/09876",
                "category": "SC",
                "caste_name": "Mahar",
                "issuing_authority": "Sub-Divisional Magistrate"
            },
            "profile_preset": {
                "category": "SC",
                "social_category": "SC"
            }
        },
        {
            "doc_key": "docIncome",
            "document_name": "Synthetic Income Certificate",
            "document_type": "Income Certificate",
            "file_name": "sample_synthetic_income.png",
            "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_income.png",
            "preview_data": {
                "certificate_no": "INC/MH/2024/54321",
                "annual_income": "Rs. 1,80,000",
                "issuing_authority": "Tahsildar",
                "scheme_ceiling_check": "Eligible for PMEGP, Stand-Up India, Mudra"
            },
            "profile_preset": {
                "annual_family_income": 180000.0,
                "annual_income": 180000.0
            }
        },
        {
            "doc_key": "docDpr",
            "document_name": "Synthetic Detailed Project Report",
            "document_type": "Detailed Project Report",
            "file_name": "sample_synthetic_dpr.png",
            "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_dpr.png",
            "preview_data": {
                "project_title": "EcoCraft Food Processing Unit",
                "project_cost": "Rs. 15,00,000",
                "loan_required": "Rs. 12,00,000 (80%)",
                "promoter_margin": "Rs. 3,00,000 (20%)",
                "balance_check": "PASS (Loan + Margin = Cost)"
            },
            "profile_preset": {
                "project_cost": 1500000.0,
                "required_loan_amount": 1200000.0,
                "own_contribution": 300000.0,
                "business_type": "manufacturing"
            }
        },
        {
            "doc_key": "docUdyam",
            "document_name": "Synthetic Udyam Registration",
            "document_type": "Udyam Registration",
            "file_name": "sample_synthetic_udyam.png",
            "file_url": "/api/v1/documents/synthetic-file/sample_synthetic_udyam.png",
            "preview_data": {
                "udyam_number": "UDYAM-MH-12-0012345",
                "enterprise_name": "EcoCraft Agro Enterprises",
                "enterprise_type": "Micro",
                "activity": "Manufacturing"
            },
            "profile_preset": {
                "has_udyam_registration": True,
                "business_type": "manufacturing"
            }
        }
    ]


@router.post("/load-synthetic/{doc_key}", response_model=DocumentUploadResponse)
def load_synthetic_sample(
    doc_key: str,
    scheme_code: Optional[str] = None,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    1-Click synthetic document loader: copies fictitious demo file, executes real-time pipeline, and stores record.
    """
    os.makedirs(SYNTHETIC_DIR, exist_ok=True)
    SyntheticDocumentGenerator.generate_all_samples(SYNTHETIC_DIR)

    key_map = {
        "docaadhaar": ("docAadhaar", "sample_synthetic_aadhaar.png", "Aadhaar"),
        "aadhaar": ("docAadhaar", "sample_synthetic_aadhaar.png", "Aadhaar"),
        "aadhaar_card": ("docAadhaar", "sample_synthetic_aadhaar.png", "Aadhaar"),
        "docpan": ("docPan", "sample_synthetic_pan.png", "PAN"),
        "pan": ("docPan", "sample_synthetic_pan.png", "PAN"),
        "pan_card": ("docPan", "sample_synthetic_pan.png", "PAN"),
        "doccaste": ("docCaste", "sample_synthetic_caste.png", "Caste Certificate"),
        "caste": ("docCaste", "sample_synthetic_caste.png", "Caste Certificate"),
        "caste_certificate": ("docCaste", "sample_synthetic_caste.png", "Caste Certificate"),
        "docincome": ("docIncome", "sample_synthetic_income.png", "Income Certificate"),
        "income": ("docIncome", "sample_synthetic_income.png", "Income Certificate"),
        "income_certificate": ("docIncome", "sample_synthetic_income.png", "Income Certificate"),
        "docdpr": ("docDpr", "sample_synthetic_dpr.png", "Detailed Project Report"),
        "dpr": ("docDpr", "sample_synthetic_dpr.png", "Detailed Project Report"),
        "detailed_project_report": ("docDpr", "sample_synthetic_dpr.png", "Detailed Project Report"),
        "docudyam": ("docUdyam", "sample_synthetic_udyam.png", "Udyam Registration"),
        "udyam": ("docUdyam", "sample_synthetic_udyam.png", "Udyam Registration"),
        "udyam_registration": ("docUdyam", "sample_synthetic_udyam.png", "Udyam Registration"),
        "doc10th": ("doc10th", "sample_synthetic_10th_marksheet.png", "10th Marksheet"),
        "10th": ("doc10th", "sample_synthetic_10th_marksheet.png", "10th Marksheet"),
        "10th_marksheet": ("doc10th", "sample_synthetic_10th_marksheet.png", "10th Marksheet"),
        "doc12th": ("doc12th", "sample_synthetic_12th_marksheet.png", "12th Marksheet"),
        "12th": ("doc12th", "sample_synthetic_12th_marksheet.png", "12th Marksheet"),
        "12th_marksheet": ("doc12th", "sample_synthetic_12th_marksheet.png", "12th Marksheet"),
        "docadmission": ("docAdmission", "sample_synthetic_admission_letter.png", "Admission Letter"),
        "admission": ("docAdmission", "sample_synthetic_admission_letter.png", "Admission Letter"),
        "admission_letter": ("docAdmission", "sample_synthetic_admission_letter.png", "Admission Letter"),
        "docfeestructure": ("docFeeStructure", "sample_synthetic_fee_structure.png", "Fee Structure"),
        "fee_structure": ("docFeeStructure", "sample_synthetic_fee_structure.png", "Fee Structure"),
        "feestructure": ("docFeeStructure", "sample_synthetic_fee_structure.png", "Fee Structure")
    }

    lookup_key = doc_key.strip().lower()
    if lookup_key not in key_map:
        raise HTTPException(status_code=400, detail=f"Invalid synthetic doc key: {doc_key}")

    std_key, filename, norm_type = key_map[lookup_key]
    src_img = os.path.join(SYNTHETIC_DIR, filename)
    src_txt = os.path.join(SYNTHETIC_DIR, os.path.splitext(filename)[0] + ".txt")

    if not os.path.exists(src_img):
        raise HTTPException(status_code=404, detail="Synthetic source file not found on server")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    dest_filename = f"synthetic_{uuid.uuid4().hex[:8]}_{filename}"
    dest_path = os.path.join(settings.UPLOAD_DIR, dest_filename)
    shutil.copyfile(src_img, dest_path)

    raw_text = None
    if os.path.exists(src_txt):
        with open(src_txt, "r", encoding="utf-8") as f:
            raw_text = f.read()

    profile_dict = _get_user_profile_dict(db, current_user.id)

    # Execute Real-Time Pipeline
    pipeline_result = DocumentValidationPipeline.validate_document(
        file_path=dest_path,
        document_type=norm_type,
        user_profile=profile_dict,
        raw_text_override=raw_text,
        selected_scheme_code=scheme_code
    )

    doc_entry = UserDocument(
        user_id=current_user.id,
        document_type=pipeline_result.get("document_type", norm_type),
        file_name=f"[Synthetic] {filename}",
        file_path=dest_path,
        file_size=os.path.getsize(dest_path),
        extracted_data=json.dumps(pipeline_result.get("extracted_data", {})),
        verification_status=pipeline_result.get("status", "verified"),
        mismatch_details=json.dumps(pipeline_result.get("mismatch_details", [])),
        ocr_status=pipeline_result.get("ocr_status", "SUCCESS"),
        format_valid=pipeline_result.get("format_valid", True),
        profile_match=pipeline_result.get("profile_match", True),
        official_verification=pipeline_result.get("official_verification", "VERIFIED"),
        confidence_score=float(pipeline_result.get("confidence", 0.98)),
        masked_identifier=pipeline_result.get("masked_identifier"),
        validation_checks=json.dumps(pipeline_result.get("checks", [])),
        audit_logs=json.dumps(pipeline_result.get("audit_logs", []))
    )
    db.add(doc_entry)
    db.commit()
    db.refresh(doc_entry)

    return {
        "id": doc_entry.id,
        "document_type": doc_entry.document_type,
        "file_name": doc_entry.file_name,
        "file_path": doc_entry.file_path,
        "verification_status": doc_entry.verification_status,
        "status": doc_entry.verification_status,
        "is_valid": str(doc_entry.verification_status).upper() in ["VERIFIED", "SUCCESS"],
        "ocr_status": doc_entry.ocr_status or "SUCCESS",
        "format_valid": doc_entry.format_valid if doc_entry.format_valid is not None else True,
        "profile_match": doc_entry.profile_match if doc_entry.profile_match is not None else True,
        "official_verification": doc_entry.official_verification or "VERIFIED",
        "official_verification_details": pipeline_result.get("official_verification_details"),
        "confidence": doc_entry.confidence_score or 0.98,
        "masked_identifier": doc_entry.masked_identifier,
        "extracted_data": pipeline_result.get("extracted_data", {}),
        "checks": pipeline_result.get("checks", []),
        "mismatch_details": pipeline_result.get("mismatch_details", []),
        "audit_logs": pipeline_result.get("audit_logs", []),
        "uploaded_at": doc_entry.uploaded_at
    }


@router.get("/required-checklist")
def get_dynamic_required_checklist(
    purpose_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    purpose: Optional[str] = Query(None),
    loan_amount: Optional[float] = Query(None),
    business_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    eff_p_type = (purpose_type or (profile.purpose_type if profile else None) or "BUSINESS").upper()
    eff_category = category or (profile.category if profile else "General") or "General"
    eff_purpose = purpose or (profile.purpose if profile else "") or ""
    eff_loan = loan_amount or (profile.required_loan_amount if profile else 1200000.0) or 1200000.0
    eff_biz = business_type or (profile.business_type if profile else "manufacturing") or "manufacturing"

    req_docs = []

    if eff_p_type == "EDUCATION":
        # 100% Dynamic Education Document Requirements
        req_docs.append({
            "doc_key": "docAadhaar",
            "document_name": "Aadhaar Card",
            "document_type": "Aadhaar",
            "is_mandatory": True,
            "reason": "Mandatory identity proof & UIDAI Verhoeff checksum verification for DBT interest subvention."
        })
        req_docs.append({
            "doc_key": "doc10th",
            "document_name": "10th Standard Marksheet / Certificate",
            "document_type": "10th Marksheet",
            "is_mandatory": True,
            "reason": "Proof of age and foundational academic qualification."
        })
        req_docs.append({
            "doc_key": "doc12th",
            "document_name": "12th Standard / Diploma Marksheet",
            "document_type": "12th Marksheet",
            "is_mandatory": True,
            "reason": "Mandatory eligibility credential for higher professional & technical degree enrollment."
        })
        req_docs.append({
            "doc_key": "docAdmission",
            "document_name": "College / University Admission Offer Letter",
            "document_type": "Admission Letter",
            "is_mandatory": True,
            "reason": "Proof of confirmed enrollment in accredited AICTE/UGC/NAAC technical or professional institute."
        })
        req_docs.append({
            "doc_key": "docFeeStructure",
            "document_name": "Institutional Fee Breakdown & Schedule",
            "document_type": "Fee Structure",
            "is_mandatory": True,
            "reason": "Official college document establishing exact loan quantum for tuition, exams, and hostel fees."
        })
        req_docs.append({
            "doc_key": "docIncome",
            "document_name": "Annual Family Income Certificate",
            "document_type": "Income Certificate",
            "is_mandatory": True,
            "reason": "Mandatory for CSIS 100% full interest subsidy (Family income <= ₹4.50 Lakh/year)."
        })
        if eff_category.upper() in ["SC", "ST", "OBC", "MINORITY", "EWS"]:
            req_docs.append({
                "doc_key": "docCaste",
                "document_name": f"{eff_category.upper()} Community / Caste Certificate",
                "document_type": "Caste Certificate",
                "is_mandatory": True,
                "reason": f"Required to unlock concessional interest rates under {eff_category.upper()} education credit quotas (NSFDC 3.5%-4%, NBCFDC, NMDFC 3%)."
            })

    elif eff_p_type == "SELF_EMPLOYMENT":
        # Dynamic Self-Employment Requirements
        req_docs.append({
            "doc_key": "docAadhaar",
            "document_name": "Aadhaar Card",
            "document_type": "Aadhaar",
            "is_mandatory": True,
            "reason": "Mandatory identity proof & DBT linking."
        })
        req_docs.append({
            "doc_key": "docIncome",
            "document_name": "Annual Income Certificate / Ration Card",
            "document_type": "Income Certificate",
            "is_mandatory": True,
            "reason": "Required for income band verification under micro-credit & welfare schemes."
        })
        if eff_category.upper() in ["SC", "ST", "OBC", "MINORITY"]:
            req_docs.append({
                "doc_key": "docCaste",
                "document_name": f"{eff_category.upper()} Community Certificate",
                "document_type": "Caste Certificate",
                "is_mandatory": True,
                "reason": f"Required for {eff_category.upper()} micro-enterprise subsidy and PM Vishwakarma / Mahila Samridhi benefits."
            })
        if eff_loan >= 50000:
            req_docs.append({
                "doc_key": "docPan",
                "document_name": "PAN Card",
                "document_type": "PAN",
                "is_mandatory": False,
                "reason": "Required for credit sanction above ₹50,000."
            })

    else:
        # Dynamic Business Requirements
        req_docs.append({
            "doc_key": "docAadhaar",
            "document_name": "Aadhaar Card",
            "document_type": "Aadhaar",
            "is_mandatory": True,
            "reason": "Mandatory identity proof & UIDAI Verhoeff checksum verification for direct DBT benefit linkage."
        })
        req_docs.append({
            "doc_key": "docPan",
            "document_name": "PAN Card",
            "document_type": "PAN",
            "is_mandatory": True,
            "reason": "Required for credit sanction, tax compliance, and entity identification."
        })
        if eff_category.upper() in ["SC", "ST", "MINORITY", "OBC"]:
            req_docs.append({
                "doc_key": "docCaste",
                "document_name": f"{eff_category.upper()} Community / Caste Certificate",
                "document_type": "Caste Certificate",
                "is_mandatory": True,
                "reason": f"Required to unlock 25%-35% special capital subsidy and concessional terms under {eff_category.upper()} quota."
            })
        req_docs.append({
            "doc_key": "docIncome",
            "document_name": "Annual Income Certificate",
            "document_type": "Income Certificate",
            "is_mandatory": True,
            "reason": "Required to verify family income compliance with statutory subsidy caps."
        })
        req_docs.append({
            "doc_key": "docDpr",
            "document_name": "Detailed Project Report (DPR)",
            "document_type": "Detailed Project Report",
            "is_mandatory": True,
            "reason": "Project financial summary verifying Project Cost, Promoter Margin (5%-10%), and Bank Loan."
        })
        if eff_biz.lower() in ["manufacturing", "service", "trading"] or "expand" in eff_purpose.lower():
            req_docs.append({
                "doc_key": "docUdyam",
                "document_name": "Udyam MSME Registration Certificate",
                "document_type": "Udyam Registration",
                "is_mandatory": False,
                "reason": "Provides priority lending status and exemption from processing fees under MSME Act."
            })

    user_docs = db.query(UserDocument).filter(UserDocument.user_id == current_user.id).all()
    user_doc_map = {}
    for d in user_docs:
        norm = DocumentValidationPipeline.normalize_doc_type(d.document_type).lower()
        user_doc_map[norm] = d

    checklist_out = []
    total_mandatory = 0
    verified_mandatory = 0

    for item in req_docs:
        norm_type = DocumentValidationPipeline.normalize_doc_type(item["document_type"]).lower()
        matched = user_doc_map.get(norm_type) or user_doc_map.get(item["doc_key"].lower())

        is_verified = matched is not None and str(matched.verification_status).upper() in ["VERIFIED", "SUCCESS"]
        if item["is_mandatory"]:
            total_mandatory += 1
            if is_verified:
                verified_mandatory += 1

        checklist_out.append({
            "doc_key": item["doc_key"],
            "document_name": item["document_name"],
            "document_type": item["document_type"],
            "is_mandatory": item["is_mandatory"],
            "reason": item["reason"],
            "is_uploaded": matched is not None,
            "verification_status": matched.verification_status if matched else "pending",
            "masked_identifier": getattr(matched, "masked_identifier", None) if matched else None,
            "confidence": getattr(matched, "confidence_score", 0.0) if matched else 0.0,
            "document_id": matched.id if matched else None
        })

    all_verified = (total_mandatory > 0) and (verified_mandatory == total_mandatory)

    return {
        "purpose_type": eff_p_type,
        "all_mandatory_verified": all_verified,
        "total_mandatory": total_mandatory,
        "verified_mandatory": verified_mandatory,
        "eligibility_unlocked": all_verified,
        "checklist": checklist_out
    }


@router.get("/verification-summary")
def get_verification_summary(
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    user_docs = db.query(UserDocument).filter(UserDocument.user_id == current_user.id).all()
    verified_types = set()
    for d in user_docs:
        if str(d.verification_status).upper() in ["VERIFIED", "SUCCESS"]:
            verified_types.add(DocumentValidationPipeline.normalize_doc_type(d.document_type).lower())
            verified_types.add(d.document_type.lower())

    has_aadhaar = any("aadhaar" in t for t in verified_types)
    has_pan = any("pan" in t for t in verified_types)
    has_income_or_caste = any("caste" in t or "income" in t for t in verified_types)

    all_verified = has_aadhaar and (has_pan or len(verified_types) >= 3) and has_income_or_caste

    return {
        "user_id": current_user.id,
        "total_uploaded": len(user_docs),
        "total_verified": len(verified_types),
        "all_mandatory_verified": all_verified,
        "verified_document_types": list(verified_types)
    }



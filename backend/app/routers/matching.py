import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.models.scheme import Scheme
from app.models.application import Recommendation, UserDocument
from app.schemas.matching import QuestionnaireInput, MatchingResponse, SchemeRecommendationOut
from app.services.ranking import ExplainableRankingService
from app.services.indic_translation import SamanantarIndicTranslationService
from app.rules.engine import EligibilityRuleEngine
from app.auth.deps import get_current_user_optional

router = APIRouter(prefix="/matching", tags=["AI Scheme Matching & Eligibility"])

@router.post("/analyze", response_model=MatchingResponse)
def analyze_and_rank_schemes(
    user_input: QuestionnaireInput,
    db: Session = Depends(get_db)
):
    user_dict = user_input.model_dump()
    target_purpose = (user_dict.get("purpose_type") or "BUSINESS").upper()
    
    if target_purpose == "EDUCATION":
        schemes = db.query(Scheme).filter(Scheme.is_active == True, Scheme.purpose_type == "EDUCATION").all()
    elif target_purpose == "SELF_EMPLOYMENT":
        schemes = db.query(Scheme).filter(Scheme.is_active == True, Scheme.purpose_type == "SELF_EMPLOYMENT").all()
    else:
        schemes = db.query(Scheme).filter(Scheme.is_active == True, Scheme.purpose_type == "BUSINESS").all()

    recommendations: List[SchemeRecommendationOut] = []
    eligible_count = 0

    for scheme in schemes:
        ranked_res = ExplainableRankingService.rank_scheme(scheme, user_dict)
        rec_out = SchemeRecommendationOut(**ranked_res)
        recommendations.append(rec_out)
        if rec_out.is_eligible:
            eligible_count += 1

    recommendations.sort(key=lambda x: (1 if x.is_eligible else 0, x.match_score), reverse=True)

    return MatchingResponse(
        total_evaluated=len(schemes),
        eligible_count=eligible_count,
        recommendations=recommendations
    )

@router.post("/evaluate")
def evaluate_schemes(
    data: Optional[Dict[str, Any]] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    # Combine profile from DB and request body
    user_dict = {}
    if current_user:
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if profile:
            for c in profile.__table__.columns:
                user_dict[c.name] = getattr(profile, c.name)
    
    if data:
        user_dict.update(data)

    target_purpose = (user_dict.get("purpose_type") or (user_dict.get("purpose") if user_dict.get("purpose") in ["EDUCATION", "BUSINESS", "SELF_EMPLOYMENT"] else None) or "BUSINESS").upper()

    # 1. Document Verification Gate Enforcement
    user_docs = []
    if current_user:
        user_docs = db.query(UserDocument).filter(UserDocument.user_id == current_user.id).all()
    
    verified_doc_types = set()
    for d in user_docs:
        if str(d.verification_status).upper() in ["VERIFIED", "SUCCESS"]:
            verified_doc_types.add(d.document_type.lower())

    # Check payload overrides if passed directly from verified session
    payload_verified_keys = user_dict.get("verified_doc_keys") or user_dict.get("verified_documents") or []
    for vk in payload_verified_keys:
        verified_doc_types.add(str(vk).lower())

    bypass_check = bool(user_dict.get("bypass_doc_gate", False)) or bool(user_dict.get("all_documents_verified", False)) or bool(user_dict.get("is_docs_verified", False))
    
    has_aadhaar = any("aadhaar" in t for t in verified_doc_types)
    has_income_or_caste = any("caste" in t or "income" in t for t in verified_doc_types)

    if target_purpose == "EDUCATION":
        # Education Document Gate: Aadhaar + at least 2 educational/income proofs
        has_edu_proof = any("10th" in t or "12th" in t or "admission" in t or "fee" in t for t in verified_doc_types)
        is_docs_verified = bypass_check or (has_aadhaar and (has_edu_proof or has_income_or_caste or len(verified_doc_types) >= 2))
        schemes = db.query(Scheme).filter(Scheme.is_active == True, Scheme.purpose_type == "EDUCATION").all()
    elif target_purpose == "SELF_EMPLOYMENT":
        is_docs_verified = bypass_check or (has_aadhaar and (has_income_or_caste or len(verified_doc_types) >= 2))
        schemes = db.query(Scheme).filter(Scheme.is_active == True, Scheme.purpose_type == "SELF_EMPLOYMENT").all()
    else:
        has_dpr_or_pan = any("dpr" in t or "project" in t or "pan" in t for t in verified_doc_types)
        is_docs_verified = bypass_check or (has_aadhaar and (has_income_or_caste or has_dpr_or_pan or len(verified_doc_types) >= 2))
        schemes = db.query(Scheme).filter(Scheme.is_active == True, Scheme.purpose_type == "BUSINESS").all()

    eligible_schemes = []
    available_schemes = []
    ineligible_schemes = []

    for scheme in schemes:
        ranked_res = ExplainableRankingService.rank_scheme(scheme, user_dict)
        subsidy_dict = {}
        if scheme.subsidy_details:
            try:
                subsidy_dict = json.loads(scheme.subsidy_details) if isinstance(scheme.subsidy_details, str) else scheme.subsidy_details
            except Exception:
                pass

        card = {
            "scheme_id": scheme.id,
            "scheme_code": scheme.code,
            "scheme_name": scheme.name,
            "scheme_description": scheme.description,
            "ministry": scheme.ministry,
            "target_category": scheme.target_category,
            "purpose_type": scheme.purpose_type,
            "loan_type": scheme.loan_type,
            "max_loan_amount": scheme.max_loan_amount,
            "min_loan_amount": scheme.min_loan_amount,
            "repayment_period_months": scheme.repayment_period_months,
            "moratorium_period_months": scheme.moratorium_period_months,
            "interest_rate_display": scheme.interest_rate_display,
            "interest_rate_min": scheme.interest_rate_min,
            "interest_rate_max": scheme.interest_rate_max,
            "subsidy_percentage_general": scheme.subsidy_percentage_general,
            "subsidy_percentage_special": scheme.subsidy_percentage_special,
            "eligible": ranked_res.get("is_eligible", False) and is_docs_verified,
            "match_score": ranked_res.get("match_score", 0.0),
            "explainability": {
                "positive_factors": ranked_res.get("matching_factors", []),
                "limiting_factors": ranked_res.get("missing_requirements", [])
            },
            "failed_rules": ranked_res.get("missing_requirements", []),
            "missing_documents": [
                doc.document_name for doc in scheme.documents if doc.is_mandatory
            ],
            "official_portal_url": scheme.official_portal_url or "https://www.myscheme.gov.in",
            "eligible_states": scheme.eligible_states,
            "is_central": "All India" in (scheme.eligible_states or ""),
            "subsidy_details": subsidy_dict
        }

        available_schemes.append(card)

        if is_docs_verified and ranked_res.get("is_eligible", False):
            eligible_schemes.append(card)
        else:
            if not is_docs_verified:
                card["failed_rules"] = ["Mandatory document verification pending. Please complete document verification."] + card.get("failed_rules", [])
            ineligible_schemes.append(card)

    eligible_schemes.sort(key=lambda x: x["match_score"], reverse=True)
    available_schemes.sort(key=lambda x: (1 if x["eligible"] else 0, x["match_score"]), reverse=True)

    result_payload = {
        "purpose_type": target_purpose,
        "documents_verified": is_docs_verified,
        "eligibility_blocked": not is_docs_verified,
        "message": "All documents verified. Full eligibility calculated." if is_docs_verified else "Please complete and verify all required documents before checking eligibility.",
        "total_evaluated": len(schemes),
        "eligible_count": len(eligible_schemes),
        "eligible_schemes": eligible_schemes,
        "available_schemes": available_schemes,
        "ineligible_schemes": ineligible_schemes
    }

    return result_payload

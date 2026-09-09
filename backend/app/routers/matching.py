import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.models.scheme import Scheme
from app.models.application import Recommendation
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
    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()
    user_dict = user_input.model_dump()

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

    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()
    
    eligible_schemes = []
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
            "max_loan_amount": scheme.max_loan_amount,
            "min_loan_amount": scheme.min_loan_amount,
            "repayment_period_months": scheme.repayment_period_months,
            "moratorium_period_months": scheme.moratorium_period_months,
            "eligible": ranked_res.get("is_eligible", False),
            "match_score": ranked_res.get("match_score", 0.0),
            "explainability": {
                "positive_factors": ranked_res.get("matching_factors", []),
                "limiting_factors": ranked_res.get("missing_requirements", [])
            },
            "failed_rules": ranked_res.get("missing_requirements", []),
            "missing_documents": [
                doc for doc in (json.loads(scheme.required_documents) if isinstance(scheme.required_documents, str) else (scheme.required_documents or []))
                if doc in ["Caste Certificate", "Project Report", "Skill Certificate"]
            ],
            "official_portal_url": scheme.official_portal_url or "https://www.myscheme.gov.in",
            "eligible_states": scheme.eligible_states,
            "is_central": "All India" in (scheme.eligible_states or ""),
            "subsidy_details": subsidy_dict
        }

        if ranked_res.get("is_eligible", False):
            eligible_schemes.append(card)
        else:
            ineligible_schemes.append(card)

    eligible_schemes.sort(key=lambda x: x["match_score"], reverse=True)

    result_payload = {
        "total_evaluated": len(schemes),
        "eligible_count": len(eligible_schemes),
        "eligible_schemes": eligible_schemes,
        "ineligible_schemes": ineligible_schemes
    }

    target_lang = user_dict.get("language") or user_dict.get("target_language") or "en"
    if target_lang != "en":
        result_payload = SamanantarIndicTranslationService.translate_scheme_evaluation(result_payload, target_lang=target_lang)

    return result_payload

@router.post("/eligibility/check/{scheme_id}")
def check_single_scheme_eligibility(
    scheme_id: int,
    user_input: QuestionnaireInput,
    db: Session = Depends(get_db)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found.")
    
    result = EligibilityRuleEngine.check_scheme_eligibility(scheme, user_input.model_dump())
    ranked = ExplainableRankingService.rank_scheme(scheme, user_input.model_dump())
    
    return {
        "scheme_id": scheme.id,
        "scheme_name": scheme.name,
        "scheme_code": scheme.code,
        "eligible": result["eligible"],
        "eligibility_score": result["score"],
        "matched_rules": result["matched_rules"],
        "failed_rules": result["failed_rules"],
        "missing_documents": result["missing_documents"],
        "compatibility_breakdown": ranked["compatibility_breakdown"],
        "matching_factors": ranked["matching_factors"],
        "missing_requirements": ranked["missing_requirements"]
    }

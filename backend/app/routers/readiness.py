from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.auth.deps import get_current_user_optional
from app.services.readiness import ApplicationReadinessService

router = APIRouter(prefix="/readiness", tags=["Application Readiness"])

@router.get("/score")
def get_readiness_score(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    user_dict = {}
    if current_user:
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if profile:
            for c in profile.__table__.columns:
                user_dict[c.name] = getattr(profile, c.name)

    readiness = ApplicationReadinessService.calculate_readiness(
        user_profile=user_dict,
        eligible_schemes_count=3,
        uploaded_documents_count=4,
        required_documents_count=5,
        selected_partner=True
    )

    return {
        "readiness_score": readiness["overall_percentage"],
        "status": "Ready for Bank Sanction" if readiness["is_ready_for_submission"] else "In Progress",
        "pillars": {
            "profile_completeness": readiness["profile_score"] * 4,
            "eligibility_validation": readiness["eligibility_score"] * 4,
            "document_verification": round((readiness["document_score"] / 35.0) * 100),
            "partner_alignment": round((readiness["partner_score"] / 15.0) * 100)
        },
        "checks": readiness["checks"]
    }

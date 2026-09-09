from typing import Dict, Any, List

class ApplicationReadinessService:
    """
    Calculates overall application readiness percentage and generates actionable recommendations.
    """

    @classmethod
    def calculate_readiness(
        cls, 
        user_profile: Dict[str, Any], 
        eligible_schemes_count: int, 
        uploaded_documents_count: int, 
        required_documents_count: int,
        selected_partner: bool = True
    ) -> Dict[str, Any]:
        
        # 1. Profile completeness (Max 25%)
        profile_score = 0
        checks = []
        
        if user_profile.get("annual_family_income", 0) > 0:
            profile_score += 7
        if user_profile.get("age", 0) >= 18:
            profile_score += 6
        if user_profile.get("purpose"):
            profile_score += 6
        if user_profile.get("location_state") or user_profile.get("state"):
            profile_score += 6
            
        profile_complete = profile_score >= 20
        checks.append({
            "title": "Profile Information",
            "score": profile_score,
            "max": 25,
            "status": "complete" if profile_complete else "incomplete",
            "message": "Personal, business and financial details are saved." if profile_complete else "Complete pending financial & business profile fields."
        })

        # 2. Eligibility Confirmation (Max 25%)
        eligibility_score = 25 if eligible_schemes_count > 0 else 10
        checks.append({
            "title": "Scheme Eligibility",
            "score": eligibility_score,
            "max": 25,
            "status": "complete" if eligible_schemes_count > 0 else "action_required",
            "message": f"Deterministic eligibility confirmed for {eligible_schemes_count} scheme(s)." if eligible_schemes_count > 0 else "Run eligibility questionnaire to find matching schemes."
        })

        # 3. Document Readiness (Max 35%)
        doc_ratio = (uploaded_documents_count / max(required_documents_count, 1)) if required_documents_count > 0 else 1.0
        doc_score = round(min(35.0, doc_ratio * 35.0), 1)
        doc_complete = doc_score >= 30
        checks.append({
            "title": "Document Verification",
            "score": doc_score,
            "max": 35,
            "status": "complete" if doc_complete else ("partial" if doc_score > 10 else "action_required"),
            "message": f"{uploaded_documents_count} of {required_documents_count} mandatory documents ready."
        })

        # 4. Partner Availability (Max 15%)
        partner_score = 15 if selected_partner else 5
        checks.append({
            "title": "Channel Partner Processing",
            "score": partner_score,
            "max": 15,
            "status": "complete" if selected_partner else "action_required",
            "message": "Authorized nodal agency / bank branch identified in your district."
        })

        overall_percentage = round(profile_score + eligibility_score + doc_score + partner_score, 1)

        return {
            "overall_percentage": min(100.0, overall_percentage),
            "profile_score": profile_score,
            "eligibility_score": eligibility_score,
            "document_score": doc_score,
            "partner_score": partner_score,
            "checks": checks,
            "is_ready_for_submission": overall_percentage >= 80.0
        }

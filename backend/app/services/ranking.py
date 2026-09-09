import json
import math
from typing import Dict, Any, List
from app.models.scheme import Scheme
from app.rules.engine import EligibilityRuleEngine

class ExplainableRankingService:
    """
    Intelligent explainable multi-factor scheme ranker.
    Weights:
      - Purpose compatibility:      25%
      - Income compatibility:       20%
      - Loan requirement match:     20%
      - Project cost compatibility: 15%
      - Location compatibility:     10%
      - Business type match:        10%
    """

    @classmethod
    def rank_scheme(cls, scheme: Scheme, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Deterministic Rule Engine Eligibility Check
        eligibility = EligibilityRuleEngine.check_scheme_eligibility(scheme, user_data)
        is_eligible = eligibility["eligible"]
        
        # 2. Factor 1: Purpose Compatibility (25%)
        user_purpose = user_data.get("purpose", "Start a Business")
        try:
            purposes = json.loads(scheme.eligible_purposes)
        except Exception:
            purposes = ["Start a Business", "Expand Existing Business"]
        
        purposes_lower = [p.lower() for p in purposes]
        if any(user_purpose.lower() in p or p in user_purpose.lower() for p in purposes_lower):
            purpose_score = 100.0
        elif "all" in purposes_lower:
            purpose_score = 90.0
        else:
            purpose_score = 30.0

        # 3. Factor 2: Income Compatibility (20%)
        user_inc = float(user_data.get("annual_family_income", 0))
        if scheme.max_income_limit and scheme.max_income_limit > 0:
            if user_inc <= scheme.max_income_limit:
                # Better score if well within target marginalized income
                ratio = user_inc / scheme.max_income_limit
                income_score = 100.0 if ratio <= 0.8 else 90.0
            else:
                income_score = max(0.0, 100.0 - ((user_inc - scheme.max_income_limit) / scheme.max_income_limit) * 100)
        else:
            # Universal scheme, no income ceiling
            income_score = 95.0

        # 4. Factor 3: Loan Requirement Match (20%)
        user_loan = float(user_data.get("required_loan_amount", 0))
        if user_loan <= 0:
            loan_score = 85.0
        elif scheme.min_loan_amount <= user_loan <= scheme.max_loan_amount:
            # Sweet spot
            loan_score = 100.0
        elif user_loan < scheme.min_loan_amount:
            loan_score = max(40.0, 100.0 - ((scheme.min_loan_amount - user_loan) / max(scheme.min_loan_amount, 1)) * 50)
        else:
            # Exceeds max loan
            loan_score = max(20.0, 100.0 - ((user_loan - scheme.max_loan_amount) / max(scheme.max_loan_amount, 1)) * 70)

        # 5. Factor 4: Project Cost Compatibility (15%)
        user_project = float(user_data.get("project_cost", 0))
        if user_project <= 0:
            project_score = 85.0
        elif scheme.min_project_cost <= user_project <= scheme.max_project_cost:
            project_score = 100.0
        elif user_project > scheme.max_project_cost:
            project_score = max(20.0, 100.0 - ((user_project - scheme.max_project_cost) / max(scheme.max_project_cost, 1)) * 80)
        else:
            project_score = 90.0

        # 6. Factor 5: Location Compatibility (10%)
        user_state = user_data.get("state", "").strip().lower()
        try:
            states = json.loads(scheme.eligible_states)
        except Exception:
            states = ["All India"]
        
        states_lower = [s.lower() for s in states]
        if "all india" in states_lower or "all" in states_lower:
            location_score = 100.0
        elif any(user_state in s or s in user_state for s in states_lower if user_state):
            location_score = 100.0
        else:
            location_score = 40.0

        # 7. Factor 6: Business Type Match (10%)
        user_biz = user_data.get("business_type", "Micro Retail").strip().lower()
        try:
            biz_types = json.loads(scheme.eligible_business_types)
        except Exception:
            biz_types = ["Manufacturing", "Service", "Trading", "Micro Retail"]
        
        biz_lower = [b.lower() for b in biz_types]
        if any(user_biz in b or b in user_biz for b in biz_lower):
            business_score = 100.0
        elif "all" in biz_lower:
            business_score = 95.0
        else:
            business_score = 45.0

        # Weighted composite score
        composite_score = (
            (purpose_score * 0.25) +
            (income_score * 0.20) +
            (loan_score * 0.20) +
            (project_score * 0.15) +
            (location_score * 0.10) +
            (business_score * 0.10)
        )

        # Apply hard eligibility penalty if deterministic rules failed
        if not is_eligible:
            final_match_score = round(min(composite_score * 0.55, 59.0), 1)
            eligibility_status = "ineligible"
        elif composite_score >= 85:
            final_match_score = round(composite_score, 1)
            eligibility_status = "eligible"
        else:
            final_match_score = round(composite_score, 1)
            eligibility_status = "partially_eligible"

        # Generate Explainable "Why Recommended" Bullet Points
        matching_factors = []
        if is_eligible:
            if income_score >= 90:
                matching_factors.append(f"Your annual family income falls comfortably within scheme eligibility guidelines.")
            if purpose_score >= 90:
                matching_factors.append(f"Your intended purpose '{user_data.get('purpose')}' is prioritized under {scheme.name}.")
            if loan_score >= 90:
                matching_factors.append(f"Requested loan amount of ₹{user_loan:,.0f} matches the sanctioned lending band (Up to ₹{scheme.max_loan_amount:,.0f}).")
            if project_score >= 90:
                matching_factors.append(f"Project cost structure of ₹{user_project:,.0f} satisfies scheme capital criteria.")
            if scheme.subsidy_percentage_general > 0 or scheme.subsidy_percentage_special > 0:
                matching_factors.append(f"Direct capital subsidy benefit of {scheme.subsidy_percentage_general:.0f}% to {scheme.subsidy_percentage_special:.0f}% available for your profile category.")
            matching_factors.append(f"Authorized channel partner network available in {user_data.get('state', 'your region')}.")
        else:
            for fr in eligibility["failed_rules"]:
                matching_factors.append(f"Notice: {fr.get('reason')}")

        # Missing Requirements / Action Items
        missing_requirements = []
        for fr in eligibility["failed_rules"]:
            missing_requirements.append(fr.get("reason"))
        for md in eligibility["missing_documents"]:
            missing_requirements.append(f"Missing Document: {md}")

        # Document readiness estimate
        total_req_docs = len(scheme.documents)
        avail_docs_count = max(0, total_req_docs - len(eligibility["missing_documents"]))
        doc_readiness = round((avail_docs_count / max(total_req_docs, 1)) * 100, 1)
        
        # Overall application readiness
        app_readiness = round(
            (100.0 if is_eligible else 40.0) * 0.40 +
            doc_readiness * 0.40 +
            (100.0 if user_data.get("profile_completed", True) else 60.0) * 0.20,
            1
        )

        return {
            "scheme_id": scheme.id,
            "scheme_code": scheme.code,
            "scheme_name": scheme.name,
            "department": scheme.department,
            "category": scheme.category,
            "description": scheme.description,
            "loan_type": scheme.loan_type,
            "max_loan_amount": scheme.max_loan_amount,
            "interest_rate_display": scheme.interest_rate_display,
            "repayment_period_months": scheme.repayment_period_months,
            "moratorium_months": scheme.moratorium_months,
            "subsidy_percentage_general": scheme.subsidy_percentage_general,
            "subsidy_percentage_special": scheme.subsidy_percentage_special,
            "subsidy_details": scheme.subsidy_details,
            "official_portal_url": scheme.official_portal_url,
            
            "match_score": final_match_score,
            "is_eligible": is_eligible,
            "eligibility_status": eligibility_status,
            
            # SHAP-Style breakdown dictionary (weights scaled 0-100)
            "compatibility_breakdown": {
                "income_compatibility": round(income_score, 1),
                "purpose_compatibility": round(purpose_score, 1),
                "loan_requirement": round(loan_score, 1),
                "project_cost": round(project_score, 1),
                "location_compatibility": round(location_score, 1),
                "business_compatibility": round(business_score, 1)
            },
            "matching_factors": matching_factors[:5],
            "missing_requirements": missing_requirements,
            "required_documents": [d.document_name for d in scheme.documents],
            "eligible_rules_count": len(eligibility["matched_rules"]),
            "failed_rules_count": len(eligibility["failed_rules"]),
            "application_readiness": app_readiness
        }

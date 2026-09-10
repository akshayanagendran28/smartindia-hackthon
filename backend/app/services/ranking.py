import json
import math
from typing import Dict, Any, List
from app.models.scheme import Scheme
from app.rules.engine import EligibilityRuleEngine

class ExplainableRankingService:
    """
    Intelligent explainable multi-factor scheme ranker for Business, Self-Employment, and Education tracks.
    """

    @classmethod
    def rank_scheme(cls, scheme: Scheme, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Deterministic Rule Engine Eligibility Check
        eligibility = EligibilityRuleEngine.check_scheme_eligibility(scheme, user_data)
        is_eligible = eligibility["eligible"]
        is_edu_scheme = getattr(scheme, "purpose_type", "BUSINESS") == "EDUCATION"
        
        # 2. Factor 1: Purpose Compatibility (25%)
        if is_edu_scheme:
            purpose_score = 100.0
        else:
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
                purpose_score = 40.0

        # 3. Factor 2: Income Compatibility (20%)
        user_inc = float(user_data.get("annual_family_income", 0) or user_data.get("annual_income", 0) or 0)
        if scheme.max_income_limit and scheme.max_income_limit > 0:
            if user_inc <= scheme.max_income_limit:
                ratio = user_inc / scheme.max_income_limit
                income_score = 100.0 if ratio <= 0.8 else 90.0
            else:
                income_score = max(0.0, 100.0 - ((user_inc - scheme.max_income_limit) / scheme.max_income_limit) * 100)
        else:
            income_score = 95.0

        # 4. Factor 3: Loan Requirement Match (20%)
        user_loan = float(user_data.get("required_loan_amount", 0) or user_data.get("loan_amount", 0) or 0)
        if user_loan <= 0:
            loan_score = 85.0
        elif scheme.min_loan_amount <= user_loan <= scheme.max_loan_amount:
            loan_score = 100.0
        elif user_loan < scheme.min_loan_amount:
            loan_score = max(40.0, 100.0 - ((scheme.min_loan_amount - user_loan) / max(scheme.min_loan_amount, 1)) * 50)
        else:
            loan_score = max(20.0, 100.0 - ((user_loan - scheme.max_loan_amount) / max(scheme.max_loan_amount, 1)) * 70)

        # 5. Factor 4: Project / Course Cost Compatibility (15%)
        if is_edu_scheme:
            annual_fee = float(user_data.get("annual_course_fee", 0.0) or 0.0)
            dur = int(user_data.get("course_duration_years", 1) or 1)
            user_project = (annual_fee * dur) if annual_fee > 0 else user_loan
        else:
            user_project = float(user_data.get("project_cost", 0) or 0)
            
        if user_project <= 0:
            project_score = 85.0
        elif scheme.min_project_cost <= user_project <= scheme.max_project_cost:
            project_score = 100.0
        elif user_project > scheme.max_project_cost:
            project_score = max(20.0, 100.0 - ((user_project - scheme.max_project_cost) / max(scheme.max_project_cost, 1)) * 80)
        else:
            project_score = 90.0

        # 6. Factor 5: Location Compatibility (10%)
        user_state = (user_data.get("location_state") or user_data.get("state") or "").strip().lower()
        try:
            states = json.loads(scheme.eligible_states)
        except Exception:
            states = ["All India"]
        
        states_lower = [s.lower() for s in states]
        if "all india" in states_lower or "all" in states_lower or not user_state:
            location_score = 100.0
        elif any(user_state in s or s in user_state for s in states_lower):
            location_score = 100.0
        else:
            location_score = 40.0

        # 7. Factor 6: Sector / Track Match (10%)
        if is_edu_scheme:
            sector_score = 100.0
        else:
            user_biz = user_data.get("business_type", "manufacturing").strip().lower()
            try:
                biz_types = json.loads(scheme.eligible_business_types)
            except Exception:
                biz_types = ["manufacturing", "service", "trading"]
            
            biz_lower = [b.lower() for b in biz_types]
            if any(user_biz in b or b in user_biz for b in biz_lower):
                sector_score = 100.0
            else:
                sector_score = 50.0

        # Calculate Weighted Aggregate Match Score
        raw_match_score = (
            (purpose_score * 0.25) +
            (income_score * 0.20) +
            (loan_score * 0.20) +
            (project_score * 0.15) +
            (location_score * 0.10) +
            (sector_score * 0.10)
        )

        if not is_eligible:
            final_match_score = min(raw_match_score * 0.5, 49.0)
        else:
            final_match_score = max(50.0, min(100.0, raw_match_score))

        # Explainability Factors
        matching_factors = [m["detail"] for m in eligibility["matched_rules"]]
        missing_reqs = [f["reason"] for f in eligibility["failed_rules"]]

        if is_eligible and is_edu_scheme:
            matching_factors.append("Eligible for full 100% interest subvention / concessional education credit.")
        elif is_eligible and scheme.subsidy_percentage_special > 0:
            matching_factors.append(f"Eligible for up to {scheme.subsidy_percentage_special:.0f}% Government capital grant/subsidy.")

        req_docs = []
        try:
            if scheme.required_documents:
                req_docs = json.loads(scheme.required_documents)
        except Exception:
            req_docs = ["Aadhaar Card", "Income Certificate"]

        return {
            "scheme_id": scheme.id,
            "scheme_code": scheme.code,
            "scheme_name": scheme.name,
            "department": scheme.department or "Government of India",
            "category": scheme.category or "Central Sector Scheme",
            "description": scheme.description or "",
            "loan_type": scheme.loan_type or "Term Loan / Subsidy",
            "max_loan_amount": float(scheme.max_loan_amount or 0.0),
            "interest_rate_display": scheme.interest_rate_display or "Concessional / Subsidized",
            "repayment_period_months": int(scheme.repayment_period_months or 84),
            "moratorium_months": int(scheme.moratorium_months or 0),
            "subsidy_percentage_general": float(scheme.subsidy_percentage_general or 0.0),
            "subsidy_percentage_special": float(scheme.subsidy_percentage_special or 0.0),
            "subsidy_details": scheme.subsidy_details or "",
            "official_portal_url": scheme.official_portal_url or "",
            "purpose_type": getattr(scheme, "purpose_type", "BUSINESS") or "BUSINESS",
            "is_eligible": is_eligible,
            "eligibility_status": "eligible" if is_eligible else "ineligible",
            "match_score": round(final_match_score, 1),
            "compatibility_breakdown": {
                "purpose": round(purpose_score, 1),
                "income": round(income_score, 1),
                "loan_amount": round(loan_score, 1),
                "project_cost": round(project_score, 1),
                "location": round(location_score, 1),
                "sector": round(sector_score, 1)
            },
            "matching_factors": matching_factors,
            "missing_requirements": missing_reqs,
            "required_documents": req_docs,
            "eligible_rules_count": len(eligibility.get("matched_rules", [])),
            "failed_rules_count": len(eligibility.get("failed_rules", [])),
            "application_readiness": 100.0 if is_eligible else 50.0
        }

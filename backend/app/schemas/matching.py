from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class QuestionnaireInput(BaseModel):
    purpose: str
    category: str = "General"
    annual_family_income: float
    project_cost: float
    required_loan_amount: float
    age: int = 25
    gender: Optional[str] = "Male"
    is_new_business: bool = True
    business_type: str = "Micro Retail"
    gstin: Optional[str] = None
    state: str = "Maharashtra"
    district: str = "Mumbai"
    available_documents: List[str] = []
    is_student: bool = False
    course: Optional[str] = None
    education_cost: float = 0.0

class CompatibilityFactor(BaseModel):
    factor_name: str
    user_value: str
    scheme_requirement: str
    score: float
    weight: float
    status: str # matched, partial, mismatched
    explanation: str

class SchemeRecommendationOut(BaseModel):
    scheme_id: int
    scheme_code: str
    scheme_name: str
    department: str
    category: str
    description: str
    loan_type: str
    max_loan_amount: float
    interest_rate_display: str
    repayment_period_months: int
    moratorium_months: int
    subsidy_percentage_general: float
    subsidy_percentage_special: float
    subsidy_details: Optional[str] = None
    official_portal_url: Optional[str] = None
    
    match_score: float # 0 to 100
    is_eligible: bool
    eligibility_status: str # eligible, partially_eligible, ineligible
    
    # SHAP-style explainable compatibility breakdown
    compatibility_breakdown: Dict[str, float]
    matching_factors: List[str]
    missing_requirements: List[str]
    required_documents: List[str]
    eligible_rules_count: int
    failed_rules_count: int
    application_readiness: float

class MatchingResponse(BaseModel):
    total_evaluated: int
    eligible_count: int
    recommendations: List[SchemeRecommendationOut]

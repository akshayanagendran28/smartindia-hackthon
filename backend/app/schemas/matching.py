from pydantic import BaseModel, model_validator
from typing import Optional, List, Dict, Any

class QuestionnaireInput(BaseModel):
    purpose: Optional[str] = "General"
    purpose_type: Optional[str] = "EDUCATION"
    category: str = "General"
    social_category: Optional[str] = None
    annual_family_income: Optional[float] = 250000.0
    annual_income: Optional[float] = 250000.0
    project_cost: Optional[float] = 500000.0
    required_loan_amount: Optional[float] = 450000.0
    loan_amount: Optional[float] = 450000.0
    age: int = 25
    gender: Optional[str] = "Male"
    is_new_business: bool = True
    business_type: Optional[str] = "Micro Retail"
    business_stage: Optional[str] = "New Greenfield Enterprise"
    gstin: Optional[str] = None
    state: str = "Maharashtra"
    district: str = "Mumbai"
    available_documents: List[str] = []
    is_student: bool = False
    course: Optional[str] = None
    education_cost: float = 0.0

    # Education specific
    current_education_level: Optional[str] = None
    course_type: Optional[str] = None
    institution_type: Optional[str] = None
    admission_status: Optional[str] = None
    annual_course_fee: Optional[float] = None
    course_duration_years: Optional[int] = None

    # Self-Employment / Artisan specific
    is_street_vendor: Optional[bool] = False
    is_artisan: Optional[bool] = False
    has_udyam_registration: Optional[bool] = False
    has_skill_training: Optional[bool] = False

    @model_validator(mode='before')
    @classmethod
    def sync_aliases(cls, values: Any) -> Any:
        if isinstance(values, dict):
            # Sync purpose_type and purpose
            if "purpose_type" in values and not values.get("purpose"):
                values["purpose"] = values["purpose_type"]
            elif "purpose" in values and not values.get("purpose_type"):
                values["purpose_type"] = values["purpose"]

            # Sync loan amounts
            la = values.get("loan_amount") or values.get("required_loan_amount") or values.get("required_loan") or 450000.0
            values["loan_amount"] = float(la)
            values["required_loan_amount"] = float(la)

            # Sync incomes
            inc = values.get("annual_income") or values.get("annual_family_income") or 250000.0
            values["annual_income"] = float(inc)
            values["annual_family_income"] = float(inc)

            # Sync project cost
            if not values.get("project_cost"):
                values["project_cost"] = values["loan_amount"]

            # Sync social category
            if values.get("social_category") and not values.get("category"):
                values["category"] = values["social_category"]
            elif values.get("category") and not values.get("social_category"):
                values["social_category"] = values["category"]

        return values

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
    purpose_type: Optional[str] = "BUSINESS"
    
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

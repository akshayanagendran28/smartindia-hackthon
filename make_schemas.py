import os

base = "C:/Users/aksha/.gemini/antigravity/scratch/scheme-sathi/backend"

def save(rel_path, content):
    full_path = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

# app/schemas/auth.py
save("app/schemas/auth.py", """from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    mobile: Optional[str] = None
    password: str
    state: Optional[str] = None
    district: Optional[str] = None
    preferred_language: Optional[str] = "en"
    role: Optional[str] = "entrepreneur"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"

class UserOut(BaseModel):
    id: int
    email: str
    mobile: Optional[str] = None
    full_name: str
    role: str
    state: Optional[str] = None
    district: Optional[str] = None
    preferred_language: str
    is_active: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

Token.model_rebuild()
""")

# app/schemas/profile.py
save("app/schemas/profile.py", """from pydantic import BaseModel
from typing import Optional
import datetime

class ProfileBase(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    category: Optional[str] = "General"
    annual_family_income: Optional[float] = 0.0
    existing_loans: Optional[float] = 0.0
    is_new_business: Optional[bool] = True
    business_type: Optional[str] = "Micro Retail"
    gstin: Optional[str] = None
    project_cost: Optional[float] = 0.0
    required_loan_amount: Optional[float] = 0.0
    purpose: Optional[str] = "Start a Business"
    is_student: Optional[bool] = False
    course: Optional[str] = None
    institution: Optional[str] = None
    education_cost: Optional[float] = 0.0
    location_state: Optional[str] = None
    location_district: Optional[str] = None
    pincode: Optional[str] = None
    profile_completed: Optional[bool] = False

class ProfileUpdate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
""")

# app/schemas/scheme.py
save("app/schemas/scheme.py", """from pydantic import BaseModel
from typing import Optional, List
import datetime

class SchemeRuleOut(BaseModel):
    id: int
    rule_name: str
    rule_code: str
    field_name: str
    operator: str
    threshold_value: str
    rule_type: str
    weight: float
    failure_reason_template: str
    is_active: bool

    class Config:
        from_attributes = True

class SchemeDocumentOut(BaseModel):
    id: int
    document_name: str
    document_type: str
    is_mandatory: bool
    description: Optional[str] = None

    class Config:
        from_attributes = True

class SchemeVersionOut(BaseModel):
    id: int
    version_number: int
    effective_from: datetime.datetime
    change_summary: str
    updated_by: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class SchemeBase(BaseModel):
    code: str
    name: str
    department: str
    category: str
    description: str
    loan_type: str
    min_loan_amount: float
    max_loan_amount: float
    min_project_cost: float
    max_project_cost: float
    min_age: int
    max_age: int
    max_income_limit: Optional[float] = None
    interest_rate_min: float
    interest_rate_max: float
    interest_rate_display: str
    repayment_period_months: int
    moratorium_months: int
    subsidy_percentage_general: float
    subsidy_percentage_special: float
    subsidy_details: Optional[str] = None
    eligible_purposes: str # JSON
    eligible_business_types: str # JSON
    eligible_categories: str # JSON
    eligible_states: str # JSON
    eligible_education: str # JSON
    is_active: bool = True
    official_portal_url: Optional[str] = None
    application_process: Optional[str] = None
    version: int = 1

class SchemeCreate(SchemeBase):
    pass

class SchemeOut(SchemeBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    rules: List[SchemeRuleOut] = []
    documents: List[SchemeDocumentOut] = []
    versions: List[SchemeVersionOut] = []

    class Config:
        from_attributes = True
""")

# app/schemas/matching.py
save("app/schemas/matching.py", """from pydantic import BaseModel
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
""")

# app/schemas/finance.py
save("app/schemas/finance.py", """from pydantic import BaseModel
from typing import Optional, List

class EmiCalculateRequest(BaseModel):
    loan_amount: float
    interest_rate_annual: float
    tenure_months: int
    moratorium_months: Optional[int] = 0

class AmortizationScheduleRow(BaseModel):
    month: int
    opening_balance: float
    emi: float
    principal_paid: float
    interest_paid: float
    closing_balance: float

class EmiCalculateResponse(BaseModel):
    loan_amount: float
    interest_rate_annual: float
    tenure_months: int
    moratorium_months: int
    monthly_emi: float
    total_interest: float
    total_repayment: float
    estimated_disclaimer: str = "All values are indicative estimates based on standard amortization schedules. Final terms depend on sanctioning authority."
    schedule_sample: List[AmortizationScheduleRow] = []
""")

# app/schemas/document.py
save("app/schemas/document.py", """from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import datetime

class DocumentUploadResponse(BaseModel):
    id: int
    document_type: str
    file_name: str
    file_path: str
    verification_status: str
    extracted_data: Dict[str, Any]
    mismatch_details: List[str]
    uploaded_at: datetime.datetime

class DocumentChecklistStatus(BaseModel):
    document_name: str
    document_type: str
    is_mandatory: bool
    is_uploaded: bool
    verification_status: str
    extracted_preview: Optional[Dict[str, Any]] = None

class SchemeDocumentReadiness(BaseModel):
    scheme_id: int
    scheme_name: str
    total_required: int
    uploaded_count: int
    readiness_percentage: float
    documents: List[DocumentChecklistStatus]
""")

# app/schemas/partner.py
save("app/schemas/partner.py", """from pydantic import BaseModel
from typing import Optional, List
import datetime

class ChannelPartnerOut(BaseModel):
    id: int
    name: str
    partner_type: str
    address: str
    state: str
    district: str
    pincode: Optional[str] = None
    latitude: float
    longitude: float
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    verification_status: str
    supported_scheme_codes: List[str] = []
    
    # Distance & Suitability
    distance_km: Optional[float] = None
    scheme_compatibility_score: Optional[float] = None
    partner_suitability_score: Optional[float] = None
    suitability_reason: Optional[str] = None

    class Config:
        from_attributes = True

class ChannelPartnerCreate(BaseModel):
    name: str
    partner_type: str
    address: str
    state: str
    district: str
    pincode: Optional[str] = None
    latitude: float
    longitude: float
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    verification_status: str = "verified"
    supported_scheme_codes: List[str] = []
""")

# app/schemas/chat.py
save("app/schemas/chat.py", """from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import datetime

class ChatMessageRequest(BaseModel):
    session_id: Optional[int] = None
    message: str
    language: str = "en" # en, hi, ta, te, kn, ml

class ChatQuickOption(BaseModel):
    label: str
    value: str
    field: Optional[str] = None

class ChatMessageResponse(BaseModel):
    session_id: int
    reply: str
    language: str
    extracted_intent: Dict[str, Any] = {}
    suggested_options: List[ChatQuickOption] = []
    recommendations: List[Dict[str, Any]] = []
""")

# app/schemas/admin.py
save("app/schemas/admin.py", """from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AdminDashboardStats(BaseModel):
    total_users: int
    total_schemes: int
    total_recommendations: int
    total_partners: int
    verified_partners: int
    total_documents: int
    pending_documents: int
    mismatched_documents: int
    
    # Analytics Charts Data
    users_by_state: List[Dict[str, Any]]
    recommendations_by_category: List[Dict[str, Any]]
    most_recommended_schemes: List[Dict[str, Any]]
    readiness_distribution: List[Dict[str, Any]]
    language_usage: List[Dict[str, Any]]

class RuleCreateRequest(BaseModel):
    scheme_id: int
    rule_name: str
    rule_code: str
    field_name: str
    operator: str
    threshold_value: str
    rule_type: str = "hard_eligibility"
    weight: float = 1.0
    failure_reason_template: str
""")

print("Schemas generated successfully!")

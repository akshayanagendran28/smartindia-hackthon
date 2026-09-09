from pydantic import BaseModel
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

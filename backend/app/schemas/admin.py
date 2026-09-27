from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import datetime

class AdminDashboardStats(BaseModel):
    # Core Aggregated Counts from DB
    total_customers: int
    active_schemes: int
    total_schemes: int
    total_applications: int
    pending_applications: int
    eligible_applications: int
    pending_invitations: int
    assigned_applications: int
    loans_under_review: int
    loans_approved: int
    loans_rejected: int
    funds_processing: int
    funds_released: int
    active_partners: int
    total_partners: int
    total_documents: int
    pending_documents: int
    
    # Financial Subsidy Aggregation
    subsidy_disbursed_text: str
    subsidy_disbursed_val: float
    estimated_subsidy_basis: str
    
    # Real Dynamic Distribution Breakdown
    users_by_state: List[Dict[str, Any]]
    demographics_distribution: List[Dict[str, Any]]
    purposes_breakdown: List[Dict[str, Any]]
    scheme_popularity: List[Dict[str, Any]]
    loan_status_distribution: List[Dict[str, Any]]
    fund_status_distribution: List[Dict[str, Any]]
    recent_audit_logs: List[Dict[str, Any]]

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

class ApplicationStatusUpdateRequest(BaseModel):
    application_status: Optional[str] = None
    loan_status: Optional[str] = None
    fund_status: Optional[str] = None
    fund_amount: Optional[float] = None
    fund_remarks: Optional[str] = None
    appointment_status: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    appointment_venue: Optional[str] = None
    appointment_remarks: Optional[str] = None
    remarks: Optional[str] = None
    reason: Optional[str] = None

class SchemeSyncRequest(BaseModel):
    source: str = "https://www.myscheme.gov.in"
    target_schemes: Optional[List[str]] = None
    force_refresh: bool = False

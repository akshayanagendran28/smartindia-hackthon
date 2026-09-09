from pydantic import BaseModel
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

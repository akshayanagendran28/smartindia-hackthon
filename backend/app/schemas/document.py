from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import datetime

class ValidationCheckItem(BaseModel):
    check_name: str
    passed: bool
    details: str

class AuditLogEntry(BaseModel):
    stage: str
    action: str
    status: str
    timestamp: str
    details: str

class DocumentUploadResponse(BaseModel):
    id: int
    document_type: str
    file_name: str
    file_path: Optional[str] = None
    verification_status: str
    status: Optional[str] = None
    ocr_status: Optional[str] = "SUCCESS"
    format_valid: Optional[bool] = True
    profile_match: Optional[bool] = True
    official_verification: Optional[str] = "VERIFIED"
    official_verification_details: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = 0.95
    masked_identifier: Optional[str] = None
    extracted_data: Dict[str, Any]
    checks: Optional[List[Dict[str, Any]]] = []
    mismatch_details: List[str] = []
    audit_logs: Optional[List[Dict[str, Any]]] = []
    uploaded_at: datetime.datetime

class DocumentValidationResponse(BaseModel):
    document_id: int
    document_type: str
    file_name: str
    status: str
    ocr_status: str
    format_valid: bool
    profile_match: bool
    official_verification: str
    official_verification_details: Optional[Dict[str, Any]] = None
    confidence: float
    checks: List[Dict[str, Any]]
    extracted_data: Dict[str, Any]
    masked_identifier: Optional[str] = None
    mismatch_details: List[str]
    audit_logs: List[Dict[str, Any]]

class DocumentChecklistStatus(BaseModel):
    document_name: str
    document_type: str
    is_mandatory: bool
    is_uploaded: bool
    verification_status: str
    file_name: Optional[str] = None
    masked_identifier: Optional[str] = None
    confidence: Optional[float] = 0.0
    extracted_preview: Optional[Dict[str, Any]] = None

class SchemeDocumentReadiness(BaseModel):
    scheme_id: int
    scheme_name: str
    total_mandatory: int
    uploaded_mandatory: int
    readiness_percentage: float
    documents: List[DocumentChecklistStatus]

class SyntheticSampleItem(BaseModel):
    doc_key: str
    document_name: str
    file_name: str
    file_url: str
    document_type: str
    preview_data: Dict[str, Any]
    profile_preset: Dict[str, Any]

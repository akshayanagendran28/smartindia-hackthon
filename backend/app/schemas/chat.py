from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import datetime

class ChatMessageRequest(BaseModel):
    session_id: Optional[int] = None
    message: str
    language: str = "en" # en, hi, ta, te, kn, ml, mr, bn, gu, pa, or, as
    scheme_code: Optional[str] = None
    scheme_id: Optional[Any] = None
    purpose_type: Optional[str] = None
    application_id: Optional[int] = None

class ChatQuickOption(BaseModel):
    label: str
    value: str
    field: Optional[str] = None
    path: Optional[str] = None

class ChatMessageResponse(BaseModel):
    session_id: int
    reply: str
    response: Optional[str] = None
    language: str
    model_used: Optional[str] = "Scheme Sathi Grounded Assistant"
    extracted_intent: Dict[str, Any] = {}
    suggested_options: List[ChatQuickOption] = []
    recommendations: List[Dict[str, Any]] = []
    scheme_recommendations: List[Dict[str, Any]] = []
    context_data: Optional[Dict[str, Any]] = None

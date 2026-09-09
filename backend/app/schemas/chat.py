from pydantic import BaseModel
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
    response: Optional[str] = None
    language: str
    model_used: Optional[str] = "Qwen via Ollama"
    extracted_intent: Dict[str, Any] = {}
    suggested_options: List[ChatQuickOption] = []
    recommendations: List[Dict[str, Any]] = []
    scheme_recommendations: List[Dict[str, Any]] = []

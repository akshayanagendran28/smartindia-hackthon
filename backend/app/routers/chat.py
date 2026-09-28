# -*- coding: utf-8 -*-
"""
AI Chat Assistant Router
Provides context-aware multilingual chat endpoints grounded in the Scheme Sathi database.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.models.scheme import Scheme
from app.models.application import (
    ChatSession, ChatMessage, SchemeApplication, UserDocument, Recommendation
)
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatQuickOption
from app.services.chat import MultilingualChatService
from app.auth.deps import get_current_user_optional

router = APIRouter(prefix="/chat", tags=["AI Chat Assistant"])

@router.post("/message", response_model=ChatMessageResponse)
@router.post("", response_model=ChatMessageResponse)
def send_chat_message(
    req: ChatMessageRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    session = None
    if req.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == req.session_id).first()
    
    if not session:
        session = ChatSession(
            user_id=current_user.id if current_user else None,
            language=req.language,
            session_title=req.message[:30] + "..." if len(req.message) > 30 else req.message
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        text=req.message,
        language=req.language
    )
    db.add(user_msg)

    # Fetch user context if logged in
    user_profile = None
    user_application = None
    user_documents = []
    user_recommendations = []

    if current_user:
        user_profile = current_user.profile or db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        
        if req.application_id:
            user_application = db.query(SchemeApplication).filter(
                SchemeApplication.id == req.application_id,
                SchemeApplication.user_id == current_user.id
            ).first()
        
        if not user_application:
            user_application = db.query(SchemeApplication).filter(
                SchemeApplication.user_id == current_user.id
            ).order_by(SchemeApplication.created_at.desc()).first()

        user_documents = db.query(UserDocument).filter(UserDocument.user_id == current_user.id).all()
        user_recommendations = db.query(Recommendation).filter(Recommendation.user_id == current_user.id).all()

    # Query verified schemes from database for factual grounding
    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()

    # Process AI Assistant Response
    ai_response = MultilingualChatService.process_message(
        user_message=req.message,
        language=req.language,
        schemes_db=schemes,
        user=current_user,
        user_profile=user_profile,
        user_application=user_application,
        user_documents=user_documents,
        user_recommendations=user_recommendations,
        scheme_code=req.scheme_code,
        scheme_id=req.scheme_id,
        purpose_type=req.purpose_type
    )

    # Save assistant message
    asst_msg = ChatMessage(
        session_id=session.id,
        sender="assistant",
        text=ai_response["reply"],
        language=ai_response["language"]
    )
    db.add(asst_msg)
    db.commit()

    return ChatMessageResponse(
        session_id=session.id,
        reply=ai_response["reply"],
        response=ai_response.get("response", ai_response["reply"]),
        language=ai_response["language"],
        model_used=ai_response.get("model_used", "Scheme Sathi Grounded Assistant"),
        extracted_intent=ai_response.get("extracted_intent", {}),
        suggested_options=ai_response.get("suggested_options", []),
        recommendations=ai_response.get("recommendations", []),
        scheme_recommendations=ai_response.get("scheme_recommendations", ai_response.get("recommendations", [])),
        context_data={
            "user_id": current_user.id if current_user else None,
            "has_application": user_application is not None,
            "application_number": user_application.application_number if user_application else None,
            "verified_documents_count": len([d for d in user_documents if (d.verification_status or "").upper() == "VERIFIED"])
        }
    )

@router.get("/suggested-prompts")
def get_suggested_prompts(
    purpose_type: Optional[str] = "BUSINESS",
    language: Optional[str] = "en"
):
    """Returns contextual suggested prompt chips for user quick-start."""
    is_edu = (purpose_type or "").upper() == "EDUCATION"
    
    if is_edu:
        prompts = [
            "What education loan schemes are available?",
            "Am I eligible for CSIS 100% interest subsidy?",
            "What documents are required for an education loan?",
            "What is my application status?",
            "Have my documents been verified?",
            "How is the EMI calculated?"
        ]
    else:
        prompts = [
            "What schemes are available for my business?",
            "What is the maximum loan amount under PMEGP?",
            "Am I eligible for PM SVANidhi?",
            "What documents are required for business loan?",
            "What is my application status?",
            "Who is my channel partner bank?"
        ]

    return {"purpose_type": purpose_type, "language": language, "prompts": prompts}

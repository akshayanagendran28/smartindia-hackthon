from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.scheme import Scheme
from app.models.application import ChatSession, ChatMessage
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.chat import MultilingualChatService

router = APIRouter(prefix="/chat", tags=["AI Chat Assistant"])

@router.post("/message", response_model=ChatMessageResponse)
def send_chat_message(
    req: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    session = None
    if req.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == req.session_id).first()
    
    if not session:
        session = ChatSession(
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

    # Query verified schemes from database for factual grounding
    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()

    # Process AI Assistant Response
    ai_response = MultilingualChatService.process_message(
        user_message=req.message,
        language=req.language,
        schemes_db=schemes
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
        model_used=ai_response.get("model_used", "Qwen via Ollama"),
        extracted_intent=ai_response.get("extracted_intent", {}),
        suggested_options=ai_response.get("suggested_options", []),
        recommendations=ai_response.get("recommendations", []),
        scheme_recommendations=ai_response.get("scheme_recommendations", ai_response.get("recommendations", []))
    )

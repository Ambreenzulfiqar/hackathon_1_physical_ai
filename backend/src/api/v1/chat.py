from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
import uuid

from ...config.database import get_async_db
from ...models.ai_chat_session import AIChatSession, AIChatMessage
from ...services.rag_service import RAGService

router = APIRouter(prefix="/chat", tags=["chat"])

class CreateSessionRequest(BaseModel):
    user_id: Optional[str] = None

class CreateSessionResponse(BaseModel):
    session_id: str
    created_at: str

class ChatMessageRequest(BaseModel):
    message: str
    context: Optional[str] = None

class ChatMessageResponse(BaseModel):
    response: str
    context_used: Optional[str] = None
    timestamp: str

@router.post("/session", response_model=CreateSessionResponse)
async def create_chat_session(
    request: CreateSessionRequest,
    db: AsyncSession = Depends(get_async_db)
) -> CreateSessionResponse:
    """
    Create a new AI chat session
    """
    try:
        # Create new chat session
        new_session = AIChatSession(
            user_id=request.user_id,
            is_active=True
        )

        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)

        return CreateSessionResponse(
            session_id=new_session.id,
            created_at=new_session.created_at.isoformat()
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating chat session: {str(e)}")


@router.post("/{session_id}/message", response_model=ChatMessageResponse)
async def send_chat_message(
    session_id: str = Path(..., description="The chat session ID"),
    request: ChatMessageRequest = Depends(),
    db: AsyncSession = Depends(get_async_db)
) -> ChatMessageResponse:
    """
    Send a message to the AI chatbot and receive a response
    """
    try:
        # Verify session exists
        result = await db.get(AIChatSession, session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Add user message to session
        user_message = AIChatMessage(
            session_id=session_id,
            role="user",
            content=request.message,
            context_used=request.context
        )
        db.add(user_message)

        # Use RAG service to generate response
        rag_service = RAGService(db)
        ai_response = await rag_service.get_response(request.message, context=request.context)

        # Add AI response to session
        ai_message = AIChatMessage(
            session_id=session_id,
            role="assistant",
            content=ai_response.response,
            context_used=ai_response.context_used
        )
        db.add(ai_message)

        await db.commit()

        return ChatMessageResponse(
            response=ai_response.response,
            context_used=ai_response.context_used,
            timestamp=ai_message.timestamp.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")
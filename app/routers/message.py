
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.crud import session as session_crud
from app.services.llm_service import generate_ai_response
from app.services.embedding_service import generate_embedding
from app.models.user import User

router = APIRouter(prefix="/sessions", tags=["Messages"])

# Schema for incoming user messages
class MessageCreate(BaseModel):
    content: str

@router.post("/{session_id}/messages")
async def send_message(
    session_id: UUID,
    message_in: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send a message to a session and generate AI response.
    """

    # 1. Verify session exists
    chat_session = await session_crud.get_session_by_id(
        db,
        session_id
    )

    if not chat_session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # 2. Verify session belongs to current user
    if chat_session.client_id != current_user.client_profile.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # 3. Save user message
    user_message = await session_crud.add_message(
        db=db,
        session_id=session_id,
        sender_type="client",
        content=message_in.content
    )

    # 4. Retrieve session history
    session_messages = await session_crud.get_session_messages(
        db,
        session_id=session_id
    )

    # 5. Format history for LLM
    chat_history = [
        {
            "role": msg.sender,
            "content": msg.content
        }
        for msg in session_messages
    ]

    # 6. Generate AI response
    system_prompt = (
        "You are an empathetic and professional psychologist "
        "helping the user."
    )

    ai_response_content = await generate_ai_response(
        chat_history,
        system_prompt=system_prompt
    )

    # 7. Save AI response
    ai_message = await session_crud.add_message(
        db=db,
        session_id=session_id,
        sender_type="ai",
        content=ai_response_content
    )

    # 8. Return both messages
    return {
        "user_message": {
            "id": str(user_message.id),
            "content": user_message.content
        },
        "ai_message": {
            "id": str(ai_message.id),
            "content": ai_message.content
        }
    }

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from uuid import UUID
from app.models.models import User, MessageSender
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageResponse,
    ChatMessageCreate,
)
from app.crud import chat as crud_chat
from app.services.ai import generate_ai_response

router = APIRouter(prefix="/chat", tags=["Chat"])


# =========================
# CREATE SESSION
# =========================
@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(
    session_in: ChatSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await crud_chat.create_chat_session(
        db=db,
        client_id=current_user.client_profile.id,
        session_in=session_in
    )


# =========================
# SEND MESSAGE + AI RESPONSE
# =========================
@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatMessageResponse
)
async def send_message(
    session_id: UUID,
    message_in: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # 1. Save user message
    user_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=message_in.content,
        sender=MessageSender.CLIENT.value
    )

    # 2. Get session history
    session_messages = await crud_chat.get_session_messages(
        db=db,
        session_id=session_id
    )

    # 3. Build chat history for AI
    chat_history = [
        {
            "role": "user" if msg.sender == MessageSender.CLIENT.value else "assistant",
            "content": msg.content
        }
        for msg in session_messages
    ]

    # 4. AI response
    ai_response_text = await generate_ai_response(chat_history)

    # 5. Save AI message
    ai_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=ai_response_text,
        sender=MessageSender.AI.value
    )

    return user_message
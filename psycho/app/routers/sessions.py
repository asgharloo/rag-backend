from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, ChatSession
from app.schemas.session import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageCreate
)
from app.dependencies import get_current_user
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/sessions",
    tags=["Chat Sessions"]
)

@router.post(
    "",
    response_model=ChatSessionResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_chat_session(
    session_in: ChatSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_session = ChatSession(
        client_id=current_user.client_profile.id  # مهم: این درست است
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    return new_session

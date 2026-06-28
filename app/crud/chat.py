#crud_chat.py
from sqlalchemy.orm import Session 
from datetime import datetime, timezone
from sqlalchemy import select, update
from app.models.models import ChatSession, ChatMessage, MessageSender
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.config import settings

async def get_session_by_id(
    db: AsyncSession,
    session_id: UUID
):
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.id == session_id)
    )

    return result.scalars().first()


async def create_chat_message(
    db: AsyncSession,
    session_id: UUID,
    content: str,
    sender: str
) -> ChatMessage:

    db_message = ChatMessage(
        session_id=session_id,
        sender=sender,
        content=content
    )

    db.add(db_message)

    await db.commit()
    await db.refresh(db_message)

    return db_message

async def get_session_messages(
    db: AsyncSession,
    session_id: UUID
):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
    )

    return result.scalars().all()

async def get_last_user_message(
    db,
    session_id
):
    stmt = (
        select(ChatMessage)
        .where(
            ChatMessage.session_id == session_id,
            ChatMessage.sender == MessageSender.CLIENT.value
        )
        .order_by(
            ChatMessage.created_at.desc()
        )
        .limit(1)
    )

    result = await db.execute(stmt)

    return result.scalar_one_or_none()

async def update_session_summary(
    db,
    session_id,
    session_summary,
    summary_version
):
    stmt = (
        update(ChatSession)
        .where(ChatSession.id == session_id)
        .values(
            session_summary=session_summary,
            summary_version=summary_version,
            summary_updated_at=datetime.now(timezone.utc)
        )
    )

    await db.execute(stmt)
    await db.commit()
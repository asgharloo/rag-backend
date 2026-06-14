from sqlalchemy.orm import Session 
from sqlalchemy import select
from app.models.models import ChatSession, ChatMessage
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

async def create_chat_session(
    db: AsyncSession,
    client_id: UUID,
    session_in: ChatSessionCreate
):
    db_session = ChatSession(
        client_id=client_id,
        title=session_in.title
    )

    db.add(db_session)

    await db.commit()
    await db.refresh(db_session)

    return db_session

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

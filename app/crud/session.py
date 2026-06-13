from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import ChatSession, ChatMessage
from uuid import UUID
import uuid
from app.schemas.chat import ChatSessionCreate


async def create_chat_session(
    db: AsyncSession,
    client_id: uuid.UUID,
    session_in: ChatSessionCreate
):
    db_session = ChatSession(
        client_id=client_id,
        title=session_in.title
    )

    print(type(db))
    
    db.add(db_session)

    await db.commit()
    await db.refresh(db_session)

    return db_session


async def get_user_sessions(db: AsyncSession, client_id: UUID):
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.client_id == client_id)
        .order_by(ChatSession.created_at.desc())
    )

    return result.scalars().all()



async def get_session_messages(db: AsyncSession, session_id: UUID):
    result = await db.execute(
        select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc())
    )
    return result.scalars().all()

async def add_message(
    db: AsyncSession,
    session_id: UUID,
    sender: str,
    content: str
):
    message = ChatMessage(
        session_id=session_id,
        sender_type=sender_type,
        content=content
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)

    return message

async def get_session_by_id(
    db: AsyncSession,
    session_id: UUID
):
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.id == session_id)
    )

    return result.scalars().first()



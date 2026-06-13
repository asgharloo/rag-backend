from sqlalchemy.orm import Session
from app.models.models import ChatSession, ChatMessage
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
import uuid

async def create_chat_session(
    db: AsyncSession,
    client_id: uuid.UUID,
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
    db: Session, 
    session_id: uuid.UUID, 
    content: str, 
    sender_type: str
) -> ChatMessage:
    """
    Saves a new chat message to the database.
    """
    db_message = ChatMessage(
        session_id=session_id,
        sender=sender_type,
        content=content
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)

    return db_message


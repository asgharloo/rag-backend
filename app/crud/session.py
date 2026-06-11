from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.models import ChatSession, ChatMessage
from uuid import UUID

def create_chat_session(db: Session, client_id: UUID, title: str = None):
    # Create the new session instance
    new_session = ChatSession(
        client_id=client_id,
        title=title
    )
    db.add(new_session)
    
    # Commit to save to the database
    db.commit()
    
    # Refresh to load the generated 'id' and 'created_at' from the database
    db.refresh(new_session)
    
    return new_session

async def get_user_sessions(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(ChatSession).where(ChatSession.client_id == user_id).order_by(ChatSession.created_at.desc())
    )
    return result.scalars().all()

    result = await db.execute(
        select(ChatSession).where(ChatSession.user_id == user_id).order_by(ChatSession.created_at.desc())
    )
    return result.scalars().all()

async def get_session_messages(db: AsyncSession, session_id: int):
    result = await db.execute(
        select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc())
    )
    return result.scalars().all()

async def add_message(db: AsyncSession, session_id: int, role: str, content: str):
    message = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


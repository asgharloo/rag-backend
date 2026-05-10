```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

# Added app. prefix
from app.database import get_db
from app.models import User, ChatSession, ChatMessage, SenderType 
from app.schemas import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionDetailResponse,
    SenderTypeEnum
)
from app.dependencies import get_current_user

# Import Mock AI service
from app.services.ai import generate_ai_response

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/sessions",
    tags=["Chat Sessions"]
)

@router.post("", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def create_chat_session(
    session_in: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_session = ChatSession(
        user_id=current_user.id,
        title=session_in.title
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    logger.info(f"New chat session created for user {current_user.id} with session ID {new_session.id}")
    return new_session

@router.get("", response_model=List[ChatSessionResponse])
def get_user_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.start_time.desc()).offset(skip).limit(limit).all()
    return sessions

@router.get("/{session_id}", response_model=ChatSessionDetailResponse)
def get_session_details(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found or access denied."
        )
    return session

@router.post("/{session_id}/messages", response_model=List[ChatMessageResponse], status_code=status.HTTP_201_CREATED)
async def send_message(
    session_id: int,
    message_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Verify session belongs to the user
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found or access denied."
        )

    # 2. Save user message
    user_message = ChatMessage(
        session_id=session.id,
        sender_type=SenderTypeEnum.USER.value,
        content=message_in.content
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # 3. Generate AI response (Mock)
    ai_content = await generate_ai_response(message_in.content) 
    # 4. Save AI message
    ai_message = ChatMessage(
        session_id=session.id,
        sender_type=SenderTypeEnum.AI.value,
        content=ai_content
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    logger.info(f"User {current_user.id} and AI exchanged messages in session {session.id}")

    # 5. Return both messages to the frontend
    return [user_message, ai_message]


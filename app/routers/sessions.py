from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dependencies import get_db, get_current_user
from app.models.models import User
from app.crud import session as crud_session
from app.schemas.session import SessionResponse, MessageResponse 

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=SessionResponse)
async def create_new_session(
    title: str = "New Counseling Session",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new chat session for the current authenticated user."""
    return await crud_session.create_chat_session(db, user_id=current_user.id, title=title)

@router.get("/", response_model=List[SessionResponse])
async def list_user_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a list of all chat sessions belonging to the current user."""
    return await crud_session.get_user_sessions(db, user_id=current_user.id)

@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve message history for a specific chat session."""
    # TODO: Verify if the session_id actually belongs to the current_user
    return await crud_session.get_session_messages(db, session_id=session_id)


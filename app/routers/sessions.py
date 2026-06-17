### app.router.sessions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.dependencies import get_db, get_current_user
from app.models.models import User
from app.crud import session as crud_session
from app.crud import chat as crud_chat
from app.schemas.chat import ChatSessionCreate
from app.schemas.session import SessionResponse, MessageResponse, SessionUpdate

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=SessionResponse)
async def create_new_session(
    title: str = "New Counseling Session",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    session_in = ChatSessionCreate(title=title)

    return await crud_session.create_chat_session(
        db=db,
        client_id=current_user.client_profile.id,
        session_in=session_in
    )
  

@router.get("/", response_model=List[SessionResponse])
async def list_user_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a list of all chat sessions belonging to the current user."""
    return await crud_session.get_user_sessions(db, client_id=current_user.client_profile.id)

@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve message history for a specific chat session."""

    session = await crud_chat.get_session_by_id(
        db,
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if session.client_id != current_user.client_profile.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return await crud_chat.get_session_messages(
        db,
     session_id
    )
     
@router.delete("/{session_id}")
async def delete_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await crud_session.delete_session(
        db=db,
        session_id=session_id,
        client_id=current_user.client_profile.id
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "message": "Session deleted successfully",
        "session_id": str(session_id)
    }

@router.patch("/{session_id}", response_model=SessionResponse)
async def rename_session(
    session_id: UUID,
    session_in: SessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await crud_session.rename_session(
        db=db,
        session_id=session_id,
        client_id=current_user.client_profile.id,
        title=session_in.title
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if result == "forbidden":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return result
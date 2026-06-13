from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app.models.models import User, ClientProfile
from app.database import get_db
from app.schemas.chat import ChatSessionCreate, ChatSessionResponse, ChatMessageResponse, ChatMessageCreate
#from app.schemas.chat import ChatMessageCreate as create_chat_message
from app.crud import chat as crud_chat
from app.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(
    session_in: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new chat session for the current authenticated user.
    """
    # Assuming current_user.id is used as the client_id
    # If you have a separate profile id, use current_user.client_profile.id instead
    chat_session = await crud_chat.create_chat_session(
        db=db, 
        client_id=current_user.client_profile.id, 
        session_in=session_in
    )
    return chat_session

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def  send_message(
    session_id: uuid.UUID,
    message_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send a new message in a specific chat session.
    """
    # 1. Save the user's message to the database
    user_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=message_in.content,
        sender_type="user"
    )
    
    # 2. AI Logic placeholder
    # Send message_in.content to LLM and get the response here
    # ai_response_text = call_llm(message_in.content, session_id)
    ai_response_text = "This is a dummy response from the AI."
    
    # 3. Save the AI's response message to the database
    ai_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=ai_response_text,
        sender_type="ai"
    )
    
    # Return the user's message (or change the response model to return both/AI message)
    return user_message


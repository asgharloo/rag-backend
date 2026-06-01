from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.dependencies import get_db, get_current_user
from app.crud import session as session_crud
from app.services.llm_service import generate_ai_response
from app.services.embedding_service import generate_embedding
from app.models.user import User

router = APIRouter(prefix="/sessions", tags=["Messages"])

# Schema for incoming user messages
class MessageCreate(BaseModel):
    content: str

@router.post("/{session_id}/messages")
async def send_message(
    session_id: int,
    message_in: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Verify session exists and belongs to the current user
    chat_session = session_crud.get_session(db, session_id=session_id)
    if not chat_session or chat_session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")

    # 2. Save user message to the database
    user_message = session_crud.create_message(
        db, 
        session_id=session_id, 
        role="user", 
        content=message_in.content
    )

    # 3. Retrieve session message history for LLM context
    session_messages = session_crud.get_session_messages(db, session_id=session_id)
    
    # Format messages for OpenAI API
    chat_history = [{"role": msg.role, "content": msg.content} for msg in session_messages]

    # 4. Generate AI response
    system_prompt = "You are an empathetic and professional psychologist helping the user."
    ai_response_content = await generate_ai_response(chat_history, system_prompt=system_prompt)

    # 5. Generate embedding for the AI response (optional, for vector search purposes)
    ai_embedding = await generate_embedding(ai_response_content)

    # 6. Save AI response to the database
    ai_message = session_crud.create_message(
        db, 
        session_id=session_id, 
        role="assistant", 
        content=ai_response_content,
        # embedding=ai_embedding  # Uncomment if create_message supports storing embeddings
    )

    return {
        "user_message": {"id": user_message.id, "content": user_message.content},
        "ai_message": {"id": ai_message.id, "content": ai_message.content}
    }


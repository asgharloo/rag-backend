#app.router.chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from uuid import UUID
from app.models.models import User, MessageSender
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageResponse,
    ChatMessageCreate,
)
from app.crud import chat as crud_chat
from app.crud import memory as crud_memory
from app.services.ai import generate_ai_response, generate_embedding
from app.services.rule_engine import (
    find_matching_rules,
    choose_best_rule
)
from datetime import datetime, timezone
import json

router = APIRouter(prefix="/chat", tags=["Chat"])


# =========================
# SEND MESSAGE + AI RESPONSE
# =========================

@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatMessageResponse
)
async def send_message(
    session_id: UUID,
    message_in: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # ==================================
    # 1. Save User Message
    # ==================================

    #### if message duplicated , should not inserted and return error to client.
    ### future should be implemeted with redis 
    
    last_message = await crud_chat.get_last_user_message(
        db=db,
        session_id=session_id
    )

    if last_message:
        is_same_content = (
            last_message.content.strip()
            == message_in.content.strip()
        )

        seconds = (
            datetime.now(timezone.utc)
            - last_message.created_at
        ).total_seconds()

        if is_same_content and seconds < 300:
            raise HTTPException(
                status_code=400,
                detail="Duplicate message"
            )
            
    user_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=message_in.content,
        sender=MessageSender.CLIENT.value
    )
    

    # ==================================
    # 2. Rule Engine
    # ==================================

    # send the request to services/rule_engine.py:
    # find_matching_rules is inside the rule_engin,py
    matches = await find_matching_rules(
        db=db,
        text=message_in.content
    )

    print("MATCHES =", matches)
    
    ## choose_best_rule.py is inside the rule_engin.py 

    winner = choose_best_rule(matches)

    print("WINNER =", winner)

    # ==================================
    # 3. Create Memory
    # ==================================
    if winner:
        embedding = await generate_embedding(
            message_in.content
        )
        # print("embeding:", embedding)
        if embedding:
            await crud_memory.create_memory(
                db=db,
                client_id=current_user.client_profile.id,
                session_id=session_id,
                content=message_in.content,
                memory_type="rule_match",
                importance_score=winner["score"],
                embedding=embedding
            )
            print("MEMORY CREATED")
    

    # ==================================
    # 4. Get Session History
    # ==================================
    session_messages = await crud_chat.get_session_messages(
        db=db,
        session_id=session_id
    )
    # ==================================
    # 5. Retrieve Memories
    # ==================================
    query_embedding = await generate_embedding(
      message_in.content
    )

    related_memories = []

    if query_embedding:
        related_memories = await crud_memory.search_memories(
        db=db,
        client_id=current_user.client_profile.id,
        query_embedding=query_embedding,
        limit=3
        )
        

    print("MEMORIES FOUND:", len(related_memories))
    print ("RELATED memories:", related_memories)

    memory_context = "\n".join(
        [
            f"- {m.memory_type}: {m.content}"
            for m in related_memories
        ]
    )
    
    print ("memory context:", memory_context) 
    # ==================================
    # 6. Build Chat History
    # ==================================
    chat_history = [
        {
            "role": (
                "user"
                if msg.sender == MessageSender.CLIENT.value
                else "assistant"
            ),
            "content": msg.content
        }
        for msg in session_messages
    ]
     
    #print ("chat_history:",chat_history)

    # ==================================
    # 7. Inject Memories Into Prompt
    # ==================================
    if memory_context:
        chat_history.insert(
            0,
            {
                "role": "system",
                "content": (
                    "Relevant user memories:\n\n"
                    f"{memory_context}\n\n"
                    "Use these memories when answering."
                )
            }
        )
    print(
        "TOTAL MESSAGES:",
        len(chat_history)
    )
    total_chars = sum(
        len(m["content"])
        for m in chat_history
    )

    print(
        "TOTAL CHARS:",
        total_chars
    )

    print(
      json.dumps(
            chat_history,
            ensure_ascii=False,
            indent=2
      )
    )
    


    # ==================================
    # 8. Generate AI Response
    # ==================================
    ai_response_text = await generate_ai_response(
        chat_history
    )
    print("AI RESPONSE:", ai_response_text)
  
    
    # ==================================
    # 9. Save AI Message
    # ==================================
    ai_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=ai_response_text,
        sender=MessageSender.AI.value
    )

    # ==================================
    # 10. Return AI Message
    # ==================================
    return ai_message
   

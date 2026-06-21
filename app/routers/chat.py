#app.router.chat.py
from fastapi import APIRouter, Depends
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
    user_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=message_in.content,
        sender=MessageSender.CLIENT.value
    )

    # ==================================
    # 2. Rule Engine
    # ==================================
    matches = await find_matching_rules(
        db=db,
        text=message_in.content
    )

    print("MATCHES =", matches)

    winner = choose_best_rule(matches)

    print("WINNER =", winner)

    # ==================================
    # 3. Create Memory
    # ==================================
    if winner:
        embedding = await generate_embedding(
            message_in.content
        )
        print("embeding:", embedding)
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
    related_memories = await crud_memory.get_memories_by_client(
        db=db,
        client_id=current_user.client_profile.id,
        limit=5
    )

    print("MEMORIES FOUND:", len(related_memories))

    memory_context = "\n".join(
        [
            f"- {m.memory_type}: {m.content}"
            for m in related_memories
        ]
    )

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
   

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
from app.config import settings
from app.services.summary import generate_session_summary
from datetime import datetime, timezone
import json

router = APIRouter(prefix="/chat", tags=["Chat"])

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
    summary = None

    # ==================================
    # 1. Check Duplicate Message
    # ==================================

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

        if (
            is_same_content
            and
            seconds < 300
        ):
            raise HTTPException(
                status_code=400,
                detail="Duplicate message"
            )
    # ==================================
    # 2. Save User Message
    # ==================================

    user_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=message_in.content,
        sender=MessageSender.CLIENT.value
    )

    # ==================================
    # 3. Generate Embedding
    # ==================================

    query_embedding = await generate_embedding(
        message_in.content
    )

    # ==================================
    # 4. Rule Engine
    # ==================================

    matches = await find_matching_rules(
        db=db,
        text=message_in.content
    )

    winner = choose_best_rule(matches)

    print("MATCHES:", matches)
    print("WINNER:", winner)

    # ==================================
    # 5. Create Memory
    # ==================================

    if winner and query_embedding:

        await crud_memory.create_memory(
            db=db,
            client_id=current_user.client_profile.id,
            session_id=session_id,
            content=message_in.content,
            memory_type="rule_match",
            importance_score=winner["score"],
            embedding=query_embedding
        )

        print("MEMORY CREATED")

    # ==================================
    # 6. Load Session Messages
    # ==================================

    session_messages = await crud_chat.get_session_messages(
        db=db,
        session_id=session_id
    )

    # ==================================
    # 7. Retrieve Related Memories
    # ==================================

    related_memories = []

    if query_embedding:

        related_memories = await crud_memory.search_memories(
            db=db,
            client_id=current_user.client_profile.id,
            query_embedding=query_embedding,
            limit=settings.MEMORY_SEARCH_LIMIT
        )
    # ==================================
    # 8. Filter Memories
    # ==================================

    filtered_memories = []

    for memory, distance in related_memories:

        print(memory.content)
        print(distance)

        if (
            distance
            <
            settings.MEMORY_DISTANCE_THRESHOLD
        ):
            filtered_memories.append(memory)

    print("MEMORIES FOUND:", len(filtered_memories))

    # ==================================
    # 9. Build Memory Context
    # ==================================

    memory_context = "\n".join(
        [
            f"- {m.memory_type}: {m.content}"
            for m in filtered_memories
        ]
    )

    # ==================================
    # 10. Build Chat History
    # ==================================

    chat_history = [

        {
            "role":
                (
                    "user"
                    if msg.sender == MessageSender.CLIENT.value
                    else "assistant"
                ),

            "content": msg.content
        }

        for msg in session_messages

    ]

    # ==================================
    # 11. Inject Memories
    # ==================================

    if memory_context:

        chat_history.insert(

            0,

            {
                "role": "system",

                "content":

                (
                    "Relevant user memories:\n\n"

                    f"{memory_context}\n\n"

                    "Use these memories when answering."
                )
            }
        )

    print(
        json.dumps(
            chat_history,
            ensure_ascii=False,
            indent=2
        )
    )

        # ==================================
    # Generate AI Response
    # ==================================

    ai_response_text = await generate_ai_response(
        chat_history
    )
    print("AI RESPONSE:", ai_response_text)

    # ==================================
    # 13. Save AI Message
    # ==================================



    ai_message = await crud_chat.create_chat_message(
        db=db,
        session_id=session_id,
        content=ai_response_text,
        sender=MessageSender.AI.value
    )

    # ==================================
    # 14. Reload Session Messages
    # ==================================

    session_messages = await crud_chat.get_session_messages(
        db=db,
        session_id=session_id
    )

    # ==================================
    # 15. Check Summary Interval
    # ==================================


    if (
        len(session_messages)
        %
        settings.SUMMARY_INTERVAL
        ==
        0
    ):

        summary_messages = [
            {
                "role": (
                    "user"
                    if msg.sender == MessageSender.CLIENT.value
                    else "assistant"
                ),
                "content": msg.content,
            }
            for msg in session_messages
        ]

        summary = await generate_session_summary(summary_messages, user_messages=summary_messages, )

    if summary:

        print(summary)

        await crud_chat.update_session_summary(
            db=db,
            session_id=session_id,
            session_summary=summary,
            summary_version=1,
        )

    return ai_message
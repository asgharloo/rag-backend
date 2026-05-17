from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import ChatSession, ChatMessage, MemoryVector
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.context_builder import ContextBuilder
from app.services.llm_service import LLMService


class ChatService:

    @staticmethod
    async def process_message(
        db: AsyncSession,
        current_user,
        session_id: str,
        user_message_content: str
    ):
        # ==============================
        # 1. Validate session
        # ==============================
        result = await db.execute(
            select(ChatSession).where(
                ChatSession.id == session_id,
                ChatSession.client_id == current_user.client_profile.id
            )
        )

        session = result.scalar_one_or_none()

        if not session:
            raise Exception("Session not found or unauthorized")

        # ==============================
        # 2. Save user message
        # ==============================
        user_message = ChatMessage(
            session_id=session.id,
            sender="client",
            content=user_message_content
        )

        db.add(user_message)
        await db.flush()

        # ==============================
        # 3. Create embedding
        # ==============================
        embedding = await EmbeddingService.create_embedding(
            user_message_content
        )

        # ==============================
        # 4. Store memory vector
        # ==============================
        memory = MemoryVector(
            client_id=session.client_id,
            session_id=session.id,
            content=user_message_content,
            embedding=embedding,
            metadata_col={
                "type": "conversation_message"
            }
        )

        db.add(memory)

        # ==============================
        # 5. Retrieve relevant memories
        # ==============================
        memories = await RetrievalService.retrieve_memories(
            db=db,
            embedding=embedding,
            client_id=session.client_id,
            limit=5
        )

        # ==============================
        # 6. Build context
        # ==============================
        context = ContextBuilder.build_context(
            user_message=user_message_content,
            retrieved_memories=memories
        )

        # ==============================
        # 7. Generate AI response
        # ==============================
        ai_response = await LLMService.generate_response([
            {
                "role": "user",
                "content": context
            }
        ])

        # ==============================
        # 8. Save AI message
        # ==============================
        ai_message = ChatMessage(
            session_id=session.id,
            sender="ai",
            content=ai_response
        )

        db.add(ai_message)

        # ==============================
        # 9. Commit all
        # ==============================
        await db.commit()

        # ==============================
        # 10. Return result
        # ==============================
        return {
            "user_message": user_message,
            "ai_message": ai_message
        }
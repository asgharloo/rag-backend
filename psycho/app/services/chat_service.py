from sqlalchemy import select

from app.models import (
    ChatSession,
    ChatMessage,
    MemoryVector
)

from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.context_builder import ContextBuilder
from app.services.llm_service import LLMService


class ChatService:

    @staticmethod
    async def process_message(
        db,
        current_user,
        session_id,
        user_message_content
    ):

        # verify session
        result = await db.execute(
            select(ChatSession).where(
                ChatSession.id == session_id
            )
        )

        session = result.scalar_one_or_none()

        if not session:
            raise Exception("Session not found")

        # save user message
        user_message = ChatMessage(
            session_id=session.id,
            sender="client",
            content=user_message_content
        )

        db.add(user_message)
        await db.flush()

        # embedding
        embedding = await EmbeddingService.create_embedding(
            user_message_content
        )

        # save memory vector
        memory = MemoryVector(
            client_id=session.client_id,
            session_id=session.id,
            content=user_message_content,
            embedding=embedding
        )

        db.add(memory)

        # retrieve memories
        memories = await RetrievalService.retrieve_memories(
            db,
            embedding
        )

        # build context
        context = ContextBuilder.build_context(
            user_message_content,
            memories
        )

        # generate AI response
        ai_response = await LLMService.generate_response([
            {
                "role": "user",
                "content": context
            }
        ])

        # save ai message
        ai_message = ChatMessage(
            session_id=session.id,
            sender="ai",
            content=ai_response
        )

        db.add(ai_message)

        await db.commit()

        return {
            "user_message": user_message,
            "ai_message": ai_message
        }
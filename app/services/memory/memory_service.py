from app.models import MemoryVector

class MemoryService:

    @staticmethod
    async def store(db, session_id, client_id, content, embedding):

        memory = MemoryVector(
            session_id=session_id,
            client_id=client_id,
            embedding=embedding,
            metadata_col={"type": "chat"}
        )

        db.add(memory)
        await db.flush()

        return memory

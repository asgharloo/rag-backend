from sqlalchemy import text


class RetrievalService:

    @staticmethod
    async def retrieve_memories(
        db,
        embedding,
        limit: int = 5
    ):

        query = text("""
        SELECT content
        FROM memory_vectors
        ORDER BY embedding <=> :embedding
        LIMIT :limit
        """)

        result = await db.execute(
            query,
            {
                "embedding": embedding,
                "limit": limit
            }
        )

        return result.fetchall()
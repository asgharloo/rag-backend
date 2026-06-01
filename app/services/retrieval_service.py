from sqlalchemy import text


class RetrievalService:

    @staticmethod
    async def retrieve_memories(db, embedding, client_id, limit=5):

        query = text("""
        SELECT 
            content,
            metadata_col,
            embedding <=> CAST(:embedding AS vector) AS distance
        FROM memory_vectors
        WHERE client_id = :client_id
        ORDER BY distance ASC
        LIMIT :limit
        """)

        result = await db.execute(query, {
            "embedding": embedding,
            "client_id": client_id,
            "limit": limit
        })

        return result.fetchall()

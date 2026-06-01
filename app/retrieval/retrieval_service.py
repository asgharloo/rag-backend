from sqlalchemy import text

class RetrievalService:

    @staticmethod
    async def search(db, embedding, client_id, limit=5):

        query = text("""
            SELECT *
            FROM memory_vectors
            WHERE client_id = :client_id
            ORDER BY embedding <-> :embedding
            LIMIT :limit
        """)

        result = await db.execute(query, {
            "client_id": client_id,
            "embedding": embedding,
            "limit": limit
        })

        return result.fetchall()

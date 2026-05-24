from openai import AsyncOpenAI
from app.config import settings


client = AsyncOpenAI(
    api_key=settings.API_KEY
)


class EmbeddingService:

    @staticmethod
    async def create_embedding(text: str) -> list[float]:

        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

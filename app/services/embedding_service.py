from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_embedding(text: str) -> list[float]:
    """
    Generates vector embeddings for a given text using OpenAI.
    """
    try:
        response = await client.embeddings.create(
            input=text,
            model="text-embedding-3-small" # or "text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Return a zero vector or raise exception based on your design
        return []

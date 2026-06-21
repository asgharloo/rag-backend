from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.BASE_URL
)


async def generate_ai_response(messages: list[dict]) -> str:

    response = await client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content



async def generate_embedding(text: str) -> list[float] | None:

    try:

        response = await client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )

        return response.data[0].embedding

    except Exception as e:

        print(f"Error generating embedding: {e}")

        return None

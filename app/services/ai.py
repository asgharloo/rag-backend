import asyncio

from openai import AsyncOpenAI
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.BASE_URL
)


async def generate_ai_response(messages):

    for attempt in range(3):

        try:
            print(">>> BEFORE OPENAI")
            response = await client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages,
                temperature=0.7,
            )
            print(">>> AFTER OPENAI")
            print(response)

            return response.choices[0].message.content

        except Exception as e:

            print(f"Attempt {attempt+1}: {e}")

            if attempt < 2:
                await asyncio.sleep(3)
            else:
                raise RuntimeError("AI request failed after 3 attempts")

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

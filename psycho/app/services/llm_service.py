from openai import AsyncOpenAI
from app.config import settings


client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY
)


SYSTEM_PROMPT = """
You are an empathetic AI psychological support assistant.

Rules:
- Be calm and emotionally supportive.
- Never shame the user.
- Avoid dangerous medical claims.
- Avoid definitive psychiatric diagnosis.
- Encourage reflection.
- Be concise but emotionally intelligent.
"""


class LLMService:

    @staticmethod
    async def generate_response(messages: list):

        response = await client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.7,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                *messages
            ]
        )

        return response.choices[0].message.content
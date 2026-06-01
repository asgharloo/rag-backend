from openai import AsyncOpenAI
from app.config import settings
import json

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class EmotionService:

    @staticmethod
    async def analyze(text: str) -> dict:

        prompt = f"""
Analyze the psychological state of this message.

Return JSON ONLY with:
- emotion (string)
- intensity (0-1)
- stress_level (0-1)
- confidence (0-1)

Message:
{text}
"""

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.choices[0].message.content)

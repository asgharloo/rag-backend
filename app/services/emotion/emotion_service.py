from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class EmotionService:

    @staticmethod
    async def analyze(text: str) -> dict:
        response = await client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a psychological emotion analyzer.

Return ONLY JSON:
{
  "emotion": "sad|happy|angry|anxious|neutral",
  "sentiment": float between -1 and 1,
  "stress": float between 0 and 1,
  "urgency": float between 0 and 1
}
"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0
        )

        return eval(response.choices[0].message.content)

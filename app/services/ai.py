import os
from openai import OpenAI
from app.config import settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)

print("OPENAI:", settings.OPENAI_API_KEY)

async def generate_ai_response(messages: list[dict]) -> str:
    """
    messages format:
    [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content

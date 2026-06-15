import os
from openai import OpenAI
from app.config import settings


async def generate_ai_response(messages: list[dict]) -> str:



    """
    messages format:
    [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
    

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    """
    client = OpenAI(
      api_key=settings.OPENAI_API_KEY,
      base_url=settings.BASE_URL
    )
    
    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content

    

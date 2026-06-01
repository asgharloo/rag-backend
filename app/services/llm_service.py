from openai import AsyncOpenAI
from app.config import settings

# Initialize the async OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_ai_response(chat_history: list[dict], system_prompt: str = None) -> str:
    """
    Generates a response from the LLM based on the chat history.
    chat_history format: [{"role": "user", "content": "hello"}, ...]
    """
    messages = []
    
    # Add system prompt if provided (e.g., "You are an empathetic psychologist...")
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
        
    messages.extend(chat_history)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini", # or "gpt-3.5-turbo" / "gpt-4"
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "Sorry, I am unable to process your request at the moment."



'''

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
'''

from app.services.ai import generate_ai_response
from app.config import settings


SYSTEM_PROMPT = f"""
You are an expert psychotherapy assistant.

Your task is to maintain a long-term summary of one therapy session.

You will receive:

1. The previous session summary (if any).
2. New messages written ONLY by the user.

Update the session summary.

Rules:

- Keep only long-term useful information.
- Keep important problems.
- Keep important life events.
- Keep important relationships.
- Keep important emotions.
- Keep medications and diagnoses if mentioned.
- Remove repeated information.
- Ignore greetings and small talk.
- Do not invent facts.
- Write in plain English.
- Maximum {settings.SUMMARY_MAX_WORDS} words.
"""

async def generate_session_summary(
    previous_summary: str | None,
    user_messages: list,
):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    if previous_summary:
        messages.append(
            {
                "role": "system",
                "content": f"""
Current session summary:

{previous_summary}

Update this summary using the new conversation below.

Do NOT rewrite the summary from scratch.
Preserve all previously important facts unless they are corrected.
Return the updated summary in Persian only.
""",
            }
        )

    messages.extend(user_messages)

    summary = await generate_ai_response(messages)

    return summary
class ContextBuilder:

    @staticmethod
    def build(user_message, retrieved_memories, emotion=None):

        memory_text = "\n".join(
            [m.content for m in retrieved_memories]
        )

        return f"""
You are a psychological AI assistant.

User message:
{user_message}

Emotion:
{emotion}

Relevant memories:
{memory_text}
"""

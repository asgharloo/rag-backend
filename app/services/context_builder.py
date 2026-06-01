class ContextBuilder:

    @staticmethod
    def build_context(
        user_message: str,
        retrieved_memories: list,
        emotion: dict
    ):

        memory_text = "\n".join([m.content for m in retrieved_memories])

        return f"""
You are a psychological AI assistant.

=== USER STATE ===
Emotion: {emotion.get('emotion')}
Stress: {emotion.get('stress_level')}
Intensity: {emotion.get('intensity')}

=== RELATED MEMORIES ===
{memory_text}

=== USER MESSAGE ===
{user_message}

Respond with empathy, clarity, and psychological awareness.
"""

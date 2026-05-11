class ContextBuilder:

    @staticmethod
    def build_context(
        user_message: str,
        retrieved_memories
    ):

        memory_context = "\n".join([
            memory.content
            for memory in retrieved_memories
        ])

        return f"""
Relevant memories:
{memory_context}

Current user message:
{user_message}
"""
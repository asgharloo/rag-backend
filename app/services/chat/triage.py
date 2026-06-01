class TriageService:

    @staticmethod
    async def classify(message: str, emotion: str = None):

        msg = message.lower()

        # 🚨 crisis detection
        if any(word in msg for word in ["suicide", "kill myself", "die"]):
            return "psychiatrist"

        # 😟 emotional distress
        if emotion in ["anxiety", "depression", "panic"]:
            return "psychologist"

        # 🙂 normal support
        return "self_help"

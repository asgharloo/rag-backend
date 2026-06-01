class ChatService:

    def __init__(
        self,
        memory_service,
        retrieval_service,
        context_service,
        llm_service,
        emotion_service,
        triage_service
    ):
        self.memory = memory_service
        self.retrieval = retrieval_service
        self.context = context_service
        self.llm = llm_service
        self.emotion = emotion_service
        self.triage = triage_service

    async def process_message(self, db, user, session_id, message):

        session = await self._get_session(db, user, session_id)

        # 1. store memory
        await self.memory.store(db, session, message)

        # 2. emotion analysis
        emotion = await self.emotion.analyze(message)

        # 3. retrieve memory
        memories = await self.retrieval.search(db, session, message)

        # 4. build context
        context = self.context.build(message, memories, emotion)

        # 5. triage decision
        triage = await self.triage.classify(message, emotion)

        # 6. LLM response
        response = await self.llm.generate(context, triage)

        # 7. save ai message
        await self.memory.store_ai(db, session, response)

        await db.commit()

        return {
            "response": response,
            "emotion": emotion,
            "triage": triage
        }

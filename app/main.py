from fastapi import FastAPI
from app.routers import auth, sessions, users,chat

app = FastAPI(title="Rag App API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Rag App API is running"}


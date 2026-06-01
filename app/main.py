from fastapi import FastAPI
from app.routers import auth, sessions, users

app = FastAPI(title="Psychology App API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sessions.router)

@app.get("/")
async def root():
    return {"message": "Psychology App API is running"}


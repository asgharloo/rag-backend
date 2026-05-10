from pydantic_settings import BaseSettings
from pathlib import Path

# پیدا کردن root پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = str(BASE_DIR / ".env")

settings = Settings()

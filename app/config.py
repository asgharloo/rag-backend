import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# دیباگ: چک کردن فایل قبل از لود شدن
env_path = ".env"
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        print("DEBUG: .env content:")
        print(f.read())
else:
    print("DEBUG: .env NOT FOUND at /app/.env")

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    BASE_URL: str
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DEBUG: bool = False
    model_config = SettingsConfigDict(
     extra="ignore",           # Ignores environment variables not defined in this class
     env_file=".env",     # Path to your .env file
     case_sensitive=False      # Makes matching case-insensitive (e.g., algorithm == ALGORITHM)
    )
 
settings = Settings()


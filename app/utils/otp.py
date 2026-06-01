# myapp/psycho/app/utils/otp.py
import redis
import random
from app.config import settings

redis_client = redis.from_url(str(settings.REDIS_URL))

#redis_client = redis.from_url(REDIS_URL)

def generate_otp() -> str:
    return str(random.randint(100000, 999999)).zfill(6)

def store_otp(phone: str, otp: str, expire: int = 120):
    redis_client.setex(f"otp:{phone}", expire, otp)

def verify_otp(phone: str, otp: str) -> bool:
    stored = redis_client.get(f"otp:{phone}")
    if stored and stored.decode() == otp:
        redis_client.delete(f"otp:{phone}")
        return True
    return False


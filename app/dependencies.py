from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from jose import JWTError, jwt
from uuid import UUID

from app.database import AsyncSessionLocal
from app.models.models import User
from app.config import settings

security = HTTPBearer()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
  
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    print("TOKEN:", token)

    try:
        token = credentials.credentials
        print("TOKEN:", token)
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        print("PAYLOAD:", payload)
        user_id = payload.get("sub")
        print("USER_ID:", user_id)    
    
        user_id = payload.get("sub")

        if not user_id:
            raise credentials_exception

        user_id = UUID(user_id)

    except (JWTError, ValueError) as e:
        print("JWT ERROR:", e)
        raise credentials_exception

    stmt = (
        select(User)
        .options(selectinload(User.client_profile))
        .where(User.id == user_id)
    )

    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise credentials_exception

    return user
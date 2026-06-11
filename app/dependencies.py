from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.database import AsyncSessionLocal
from app.utils.jwt import verify_token
from app.crud.user import get_user_by_id
from app.models.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from jose import JWTError, jwt
from app.config import settings

security = HTTPBearer()


async def get_db():
    """
    Dependency to get the database session.
    Yields the session and closes it automatically after the request.
    """
    async with AsyncSessionLocal() as session:
        yield session

    # Verify and decode the token

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

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    stmt = (
        select(User)
        .options(joinedload(User.client_profile))
        .where(User.id == user_id)   
    )

    result = await db.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user


    return user



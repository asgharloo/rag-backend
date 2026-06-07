from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.database import AsyncSessionLocal
from app.utils.jwt import verify_token
from app.crud.user import get_user_by_id
from app.models.models import User

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
    """
    Dependency to get the current authenticated user from the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # استخراج توکن از هدر
    token = credentials.credentials

    # Verify and decode the token
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    # Extract user ID from the token payload (assuming it's stored in 'sub')

    user_id: str = payload.get("sub")  
    
    if user_id is None:
        raise credentials_exception

    # Fetch user from database
    user = await get_user_by_id(db, user_id=user_id)
    
    if user is None:
        raise credentials_exception

    return user


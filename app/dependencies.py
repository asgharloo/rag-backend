from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.database import AsyncSessionLocal
from app.utils.jwt import verify_token
from app.crud.user import get_user_by_id
from app.models.models import User

# Defines the scheme for extracting the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/verify-otp")

async def get_db():
    """
    Dependency to get the database session.
    Yields the session and closes it automatically after the request.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
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
    
    # Verify and decode the token
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
        
    # Extract user ID from the token payload (assuming it's stored in 'sub')
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
        
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception

    # Fetch user from database
    user = await get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
        
    return user


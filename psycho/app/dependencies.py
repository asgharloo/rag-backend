# app/dependencies.py

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database import get_db
from app.models import User

# The tokenUrl should match the endpoint where the client sends the OTP to get the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/verify-otp")

# Fetch environment variables with fallback defaults
SECRET_KEY = os.getenv("SECRET_KEY", "eJ4Khu2kPZbnhmUEOPZFaMnOL46mqxojps1Jgni-5Jk")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Dependency to extract and validate the JWT token from the request header.
    Returns the current authenticated User object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token using the secret key from environment variables
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = str(payload.get("sub"))
        
        if user_id is None:
            raise credentials_exception
    except JWTError:
        # Catch any JWT decoding errors (e.g., expired token, invalid signature)
        raise credentials_exception
        
    # Query the user from the database
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
        
    return user


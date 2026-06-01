
# routers/users.py

from fastapi import APIRouter, Depends
from app.schemas.user import UserMeResponse
from app.models.models import User
from app.dependencies import get_current_user

# Initialize the router for user-related endpoints
router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserMeResponse)
def get_user_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.
    
    Returns the details of the currently logged-in user based on their JWT token.
    If the user has an associated client profile, it will be included in the response.
    """
    # The get_current_user dependency handles token validation and fetching the user from the database.
    # We simply return the fetched user object. The response_model handles serialization.
    return current_user



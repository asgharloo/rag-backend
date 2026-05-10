
# psycho/app/routers/auth.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User
from app.schemas.auth import PhoneNumberRequest, VerifyOTPRequest, TokenResponse
from app.utils.otp import generate_otp, store_otp, verify_otp
from app.utils.jwt import create_access_token

# Use logger instead of print
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(request: PhoneNumberRequest):
    """Generate and send OTP to the user's phone number."""
    otp = generate_otp()
    store_otp(request.phone_number, otp)
    
    # In production, this should be replaced with an actual SMS provider
    logger.info(f"OTP for {request.phone_number}: {otp}")
    logger.warning(f"Development OTP for {request.phone_number}: {otp}")
    
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def verify_otp_endpoint(request: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    """Verify the OTP code and login or register the user."""
    if not verify_otp(request.phone_number, request.otp_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    user = await _get_or_create_user(db, request.phone_number)
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return TokenResponse(access_token=access_token, token_type="bearer")


# --- Helper Functions ---

async def _get_or_create_user(db: AsyncSession, phone_number: str) -> User:
    """Helper function to find an existing user or create a new one in the database."""
    result = await db.execute(select(User).where(User.phone_number == phone_number))
    user = result.scalar_one_or_none()

    if not user:
        user = User(phone_number=phone_number,role=UserRole.CLIENT)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    return user


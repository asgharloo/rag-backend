# psycho/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.models.models import User

from app.database import get_db
from app.schemas.auth import PhoneNumberRequest, VerifyOTPRequest, TokenResponse
from app.crud import user as crud_user
from app.utils.otp import generate_otp, store_otp, verify_otp
from app.utils.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/send-otp")
async def send_otp(request: PhoneNumberRequest, db: AsyncSession = Depends(get_db)) -> Any:
    # تولید و ذخیره در ردیس
    otp_code = generate_otp()
    store_otp(request.phone_number, otp_code)

    # TODO: ارسال واقعی کد با سرویس پیامک
    print(f"--> SIMULATED SMS: OTP for {request.phone_number} is {otp_code}")

    return {"message": "OTP sent successfully"}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp_endpoint(request: VerifyOTPRequest, db: AsyncSession = Depends(get_db)) -> Any:
    # بررسی کد در ردیس
    is_valid = verify_otp(request.phone_number, request.otp_code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP code"
        )

    # گرفتن یا ساختن کاربر
    user = await crud_user.get_user_by_phone(db, phone_number=request.phone_number)
    if not user:
        user = await crud_user.create_user(db, phone_number=request.phone_number)

    # تولید توکن واقعی با jwt.py شما
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

###  from here was before code
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


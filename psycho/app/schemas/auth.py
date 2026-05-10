from pydantic import BaseModel, Field

class PhoneNumberRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^09\d{9}$")

class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp_code: str = Field(..., min_length=6, max_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

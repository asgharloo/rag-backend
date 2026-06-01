import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.models import UserRole

class ClientProfileResponse(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserMeResponse(BaseModel):
    id: uuid.UUID
    phone_number: str
    role: UserRole
    is_active: bool
    client_profile: Optional[ClientProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)


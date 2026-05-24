import uuid
from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict

# Assuming UserRole is imported from your models
from app.models import UserRole 
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid

class SenderTypeEnum(str, Enum):
    USER = "user"
    AI = "ai"
    SYSTEM = "system"

# Define SenderType Enum for Pydantic validation
class SenderType(str, Enum):
    USER = "USER"
    AI = "AI"
# Schema for incoming user message
class ChatMessageCreate(BaseModel):
    content: str

# Schema for outgoing message response (both User and AI)
class ChatMessageResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    sender_type: SenderType
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- Profile and User Schemas ---

class ClientProfileResponse(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    marital_status: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class UserMeResponse(BaseModel):
    id: uuid.UUID  # Changed from int to uuid.UUID
    phone_number: str
    role: UserRole 
    is_active: bool
    client_profile: Optional[ClientProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)

# --- Chat Session Schemas ---

class ChatSessionCreate(BaseModel):
    title: Optional[str] = "New Chat"

class ChatSessionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]

    model_config = ConfigDict(from_attributes=True) # Updated to Pydantic V2 style

class ChatMessageResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    sender_type: SenderTypeEnum 
    content: str
    created_at: datetime 

    model_config = ConfigDict(from_attributes=True) # Updated to Pydantic V2 style

# Response schema for getting a session with its messages
class ChatSessionDetailResponse(ChatSessionResponse):
    messages: List[ChatMessageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

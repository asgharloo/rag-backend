from pydantic import BaseModel, UUID4, ConfigDict
from datetime import datetime
from typing import Optional


# --- Chat Session Schemas ---
class ChatSessionCreate(BaseModel):
    title: Optional[str] = "گفتگوی جدید"


class ChatSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    client_id: UUID4
    title: str
    created_at: datetime


# --- Chat Message Schemas ---
class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    session_id: UUID4
    sender_type: str
    content: str
    created_at: datetime


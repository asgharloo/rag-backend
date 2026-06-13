
### `app/schemas/session.py`
from pydantic import BaseModel, ConfigDict, UUID4
from datetime import datetime
from typing import List, Optional


# ==========================================
# ChatMessage Schemas
# ==========================================
class MessageBase(BaseModel):
    sender: str  # e.g., "user" or "assistant"
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: UUID4
    session_id: UUID4
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Chat Session Schemas
# ==========================================
class SessionBase(BaseModel):
    title: str

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: UUID4
    client_id: UUID4
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Optional: If you want to return a session along with all its messages
class SessionWithMessagesResponse(SessionResponse):
    messages: List[MessageResponse] = []

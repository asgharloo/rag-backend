
### `app/schemas/session.py`
```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

# ==========================================
# Message Schemas
# ==========================================
class MessageBase(BaseModel):
    role: str  # e.g., "user" or "assistant"
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    session_id: int
    created_at: datetime

    # This allows Pydantic to read data from SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Chat Session Schemas
# ==========================================
class SessionBase(BaseModel):
    title: str

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Optional: If you want to return a session along with all its messages
class SessionWithMessagesResponse(SessionResponse):
    messages: List[MessageResponse] = []
```

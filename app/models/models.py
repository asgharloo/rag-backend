from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid
import enum

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    TIMESTAMP,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pgvector.sqlalchemy import Vector

from app.database import Base


# =========================
# ENUMS
# =========================

class UserRole(str, enum.Enum):
    CLIENT = "client"
    SPECIALIST = "specialist"
    ADMIN = "admin"


class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    ENDED = "ended"
    ARCHIVED = "archived"


class MessageSender(str, enum.Enum):
    CLIENT = "client"
    AI = "ai"


class MemoryType(str, enum.Enum):
    CHAT = "chat"
    PERSONAL = "personal"
    CLINICAL = "clinical"
    INSIGHT = "insight"


class ImportanceLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# =========================
# MIXIN
# =========================

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.utcnow,
    )


# =========================
# USER
# =========================

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    role: Mapped[UserRole] = mapped_column(String, default=UserRole.CLIENT.value)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    client_profile: Mapped[Optional["ClientProfile"]] = relationship(
        back_populates="user",
        uselist=False,
    )

    specialist_profile: Mapped[Optional["SpecialistProfile"]] = relationship(
        back_populates="user",
        uselist=False,
    )


class ClientProfile(TimestampMixin, Base):
    __tablename__ = "client_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )

    memories: Mapped[list["Memory"]] = relationship(
        "Memory", 
        back_populates="client",
        cascade="all, delete-orphan"
    )

    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))

    user: Mapped["User"] = relationship(back_populates="client_profile")

    chat_sessions: Mapped[List["ChatSession"]] = relationship(back_populates="client")
    
    #memories: Mapped[List["Memory"]] = relationship(back_populates="client")


class SpecialistProfile(TimestampMixin, Base):
    __tablename__ = "specialist_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )

    specialization: Mapped[str] = mapped_column(String(120))

    user: Mapped["User"] = relationship(back_populates="specialist_profile")


# =========================
# CHAT
# =========================

class ChatSession(TimestampMixin, Base):
    __tablename__ = "chat_sessions"
   
    title: Mapped[Optional[str]] = mapped_column(
        String, 
        default="جلسه جدید"
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True,
    )

    status: Mapped[SessionStatus] = mapped_column(
        String,
        default=SessionStatus.ACTIVE.value,
    )

    summary: Mapped[Optional[str]] = mapped_column(Text)

    client: Mapped["ClientProfile"] = relationship(back_populates="chat_sessions")
    messages: Mapped[List["ChatMessage"]] = relationship(back_populates="session")


class ChatMessage(TimestampMixin, Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True,
    )

    sender: Mapped[MessageSender] = mapped_column(String, nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    metadata_col: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)

    session: Mapped["ChatSession"] = relationship(back_populates="messages")


# =========================
# 🧠 MEMORY (AI CORE)
# =========================

class Memory(TimestampMixin, Base):
    __tablename__ = "memories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True,
    )

    session_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True,
    )

    # This must match the variable name in ClientProfile
    client: Mapped["ClientProfile"] = relationship(
        "ClientProfile",
        back_populates="memories"
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    embedding: Mapped[list[float]] = mapped_column(Vector(1536))

    # 🧠 NEW: emotional intelligence
    emotion: Mapped[Optional[str]] = mapped_column(String(50))  
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float)  # -1 to +1

    # 🧠 NEW: psychological intensity
    stress_level: Mapped[Optional[float]] = mapped_column(Float)  # 0-1
    urgency_score: Mapped[Optional[float]] = mapped_column(Float)  # 0-1

    memory_type: Mapped[str] = mapped_column(String, default="chat")

    importance_score: Mapped[float] = mapped_column(Float, default=0.5)

    # 🧠 NEW: decay system (very important)
    decay_score: Mapped[float] = mapped_column(Float, default=1.0)

    metadata_col: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)

# =========================
# VECTOR INDEX (pgvector)
# =========================

Index(
    "idx_memory_embedding",
    Memory.embedding,
    postgresql_using="hnsw",
    postgresql_ops={"embedding": "vector_cosine_ops"},
)

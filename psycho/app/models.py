# psycho/app/models.py

from datetime import datetime
from typing import Optional, Any
import uuid
import enum

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    TIMESTAMP,
    text,
    UUID,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pgvector.sqlalchemy import Vector

from app.database import Base


# ==================== ENUMS ====================

class UserRole(str, enum.Enum):
    CLIENT = "client"
    SPECIALIST = "specialist"
    ADMIN = "admin"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class MaritalStatus(str, enum.Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    ENDED = "ended"
    ARCHIVED = "archived"


class MessageSender(str, enum.Enum):
    CLIENT = "client"
    AI = "ai"


class AssessmentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class SpecialistStatus(str, enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TestType(str, enum.Enum):
    DEPRESSION = "depression"
    ANXIETY = "anxiety"
    PERSONALITY = "personality"
    OTHER = "other"


class PrescriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RecommendationType(str, enum.Enum):
    LIFESTYLE = "lifestyle"
    THERAPY = "therapy"
    MEDICATION = "medication"
    OTHER = "other"


# ==================== MIXIN ====================

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


# ==================== MODELS ====================

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(
            UserRole,
            name="user_role",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=UserRole.CLIENT,
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(String(15), unique=True, index=True)

    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

    client_profile: Mapped[Optional["ClientProfile"]] = relationship(
        back_populates="user", uselist=False
    )

    specialist_profile: Mapped[Optional["SpecialistProfile"]] = relationship(
        back_populates="user", uselist=False
    )


class ClientProfile(TimestampMixin, Base):
    __tablename__ = "client_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))

    date_of_birth: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))

    gender: Mapped[Optional[Gender]] = mapped_column(
        SQLEnum(Gender, name="gender_type", values_callable=lambda x: [e.value for e in x])
    )

    marital_status: Mapped[Optional[MaritalStatus]] = mapped_column(
        SQLEnum(
            MaritalStatus,
            name="marital_status_type",
            values_callable=lambda x: [e.value for e in x],
        )
    )

    occupation: Mapped[Optional[str]] = mapped_column(String(100))
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(15))

    user: Mapped["User"] = relationship(back_populates="client_profile")

    clinical_profile: Mapped[Optional["ClientClinicalProfile"]] = relationship(
        back_populates="client", uselist=False
    )

    chat_sessions: Mapped[list["ChatSession"]] = relationship(back_populates="client")
    assessments: Mapped[list["ClientAssessment"]] = relationship(back_populates="client")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="client")
    test_results: Mapped[list["TestResult"]] = relationship(back_populates="client")
    prescriptions: Mapped[list["Prescription"]] = relationship(back_populates="client")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="client")


class ClientClinicalProfile(TimestampMixin, Base):
    __tablename__ = "client_clinical_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"), unique=True
    )

    medical_history: Mapped[Optional[dict]] = mapped_column(JSONB)
    current_medications: Mapped[Optional[dict]] = mapped_column(JSONB)
    allergies: Mapped[Optional[dict]] = mapped_column(JSONB)
    previous_diagnoses: Mapped[Optional[dict]] = mapped_column(JSONB)
    family_history: Mapped[Optional[dict]] = mapped_column(JSONB)

    client: Mapped["ClientProfile"] = relationship(back_populates="clinical_profile")


class ChatSession(TimestampMixin, Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"), index=True
    )

    status: Mapped[SessionStatus] = mapped_column(
        SQLEnum(SessionStatus, name="session_status",
        values_callable=lambda x: [e.value for e in x]),
        default=SessionStatus.ACTIVE,
    )

    started_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    ended_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))

    client: Mapped["ClientProfile"] = relationship(back_populates="chat_sessions")

    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="session")

    summary: Mapped[Optional["SessionSummary"]] = relationship(
        back_populates="session",
        uselist=False
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True
    )

    sender: Mapped[MessageSender] = mapped_column(
        SQLEnum(MessageSender, name="message_sender",
        values_callable=lambda x: [e.value for e in x]),
        nullable=False
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    metadata_col: Mapped[Optional[dict]] = mapped_column("metadata", JSONB)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    session: Mapped["ChatSession"] = relationship(back_populates="messages")


class SessionSummary(TimestampMixin, Base):
    __tablename__ = "session_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        unique=True
    )

    summary: Mapped[str] = mapped_column(Text, nullable=False)

    key_topics: Mapped[Optional[dict]] = mapped_column(JSONB)
    sentiment_analysis: Mapped[Optional[dict]] = mapped_column(JSONB)

    session: Mapped["ChatSession"] = relationship(back_populates="summary")


class MemoryVector(Base):
    __tablename__ = "memory_vectors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete
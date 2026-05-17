
# psycho/app/models.py
from datetime import datetime
from typing import Any, Optional
import uuid
import enum
from sqlalchemy import text 
from sqlalchemy import Enum
import pgvector 

from pgvector.sqlalchemy import Vector
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    CheckConstraint,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
    UUID,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.database import Base

from sqlalchemy import Enum as SQLEnum


# ==================== ENUMS ====================

user_role_enum = ENUM(
    "client", "specialist", "admin",
    name="user_role",
    create_type=False
)

gender_enum = ENUM(
    "male", "female", "other",
    name="gender_type",
    create_type=False
)

marital_status_enum = ENUM(
    "single", "married", "divorced", "widowed",
    name="marital_status_type",
    create_type=False
)

session_status_enum = ENUM(
    "active", "ended", "archived",
    name="session_status",
    create_type=False
)

message_sender_enum = ENUM(
    "client", "ai",
    name="message_sender",
    create_type=False
)

assessment_status_enum = ENUM(
    "pending", "completed",
    name="assessment_status",
    create_type=False
)

specialist_status_enum = ENUM(
    "available", "busy", "offline",
    name="specialist_status",
    create_type=False
)

appointment_status_enum = ENUM(
    "scheduled", "completed", "cancelled",
    name="appointment_status",
    create_type=False
)

test_type_enum = ENUM(
    "depression", "anxiety", "personality", "other",
    name="test_type",
    create_type=False
)

prescription_status_enum = ENUM(
    "active", "completed", "cancelled",
    name="prescription_status",
    create_type=False
)

recommendation_type_enum = ENUM(
    "lifestyle", "therapy", "medication", "other",
    name="recommendation_type",
    create_type=False
)


# ==================== MODELS ====================
class UserRole(str,enum.Enum):
    CLIENT = "client"
    SPECIALIST = "specialist"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    role: Mapped[UserRole] = mapped_column(
    Enum(
        UserRole, 
        name="user_role", 
        native_enum=True, 
        values_callable=lambda obj: [e.value for e in obj] # <--- Add this line
    ),
    default=UserRole.CLIENT,
    nullable=False
    )
     
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    phone_number: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    client_profile: Mapped[Optional["ClientProfile"]] = relationship(
        back_populates="user", uselist=False
    )
    specialist_profile: Mapped[Optional["SpecialistProfile"]] = relationship(
        back_populates="user", uselist=False
    )


class ClientProfile(Base):
    __tablename__ = "client_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )

    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(gender_enum, nullable=True)
    marital_status: Mapped[Optional[str]] = mapped_column(marital_status_enum, nullable=True)
    occupation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
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


class ClientClinicalProfile(Base):
    __tablename__ = "client_clinical_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        unique=True
    )
    medical_history: Mapped[Optional[Any]] = mapped_column("medical_history", JSONB)
    current_medications: Mapped[Optional[Any]] = mapped_column("current_medications", JSONB)
    allergies: Mapped[Optional[Any]] = mapped_column("allergies", JSONB)
    previous_diagnoses: Mapped[Optional[Any]] = mapped_column("previous_diagnoses", JSONB)
    family_history: Mapped[Optional[Any]] = mapped_column("family_history", JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    client: Mapped["ClientProfile"] = relationship(back_populates="clinical_profile")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True
    )
    status: Mapped[str] = mapped_column(
        session_status_enum,
        server_default=text("'active'")
    )
    started_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    client: Mapped["ClientProfile"] = relationship(back_populates="chat_sessions")
    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="session")
    summary: Mapped[Optional["SessionSummary"]] = relationship(
        back_populates="session", uselist=False
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True
    )
    sender: Mapped[str] = mapped_column(message_sender_enum, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_col: Mapped[Optional[Any]] = mapped_column("metadata", JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    session: Mapped["ChatSession"] = relationship(back_populates="messages")


class SessionSummary(Base):
    __tablename__ = "session_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        unique=True
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_topics: Mapped[Optional[Any]] = mapped_column("key_topics", JSONB)
    sentiment_analysis: Mapped[Optional[Any]] = mapped_column("sentiment_analysis", JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    session: Mapped["ChatSession"] = relationship(back_populates="summary")


class MemoryVector(Base):
    __tablename__ = "memory_vectors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True
    )


    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Any] = mapped_column(Vector(1536), nullable=False)
    metadata_col: Mapped[Optional[Any]] = mapped_column("metadata", JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    __table_args__ = (
        Index(
            "memory_vectors_embedding_idx",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"}
        ),
    )


class MemoryRetrievalLog(Base):
    __tablename__ = "memory_retrieval_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True
    )
    query: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_memories: Mapped[Optional[Any]] = mapped_column("retrieved_memories", JSONB)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )


class AssessmentCategory(Base):
    __tablename__ = "assessment_categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    assessments: Mapped[list["ClientAssessment"]] = relationship(back_populates="category")


class ClientAssessment(Base):
    __tablename__ = "client_assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True
    )
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("assessment_categories.id", ondelete="SET NULL"),
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        assessment_status_enum,
        server_default=text("'pending'")
    )
    responses: Mapped[Optional[Any]] = mapped_column("responses", JSONB)
    score: Mapped[Optional[float]] = mapped_column(Float)
    interpretation: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    client: Mapped["ClientProfile"] = relationship(back_populates="assessments")
    category: Mapped[Optional["AssessmentCategory"]] = relationship(back_populates="assessments")
    services: Mapped[list["AssessmentService"]] = relationship(back_populates="assessment")


class AssessmentService(Base):
    __tablename__ = "assessment_services"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_assessments.id", ondelete="CASCADE"),
        index=True
    )
    service_name: Mapped[str] = mapped_column(String(100), nullable=False)
    service_description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    assessment: Mapped["ClientAssessment"] = relationship(back_populates="services")


class SpecialistProfile(Base):
    __tablename__ = "specialist_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=False)
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        specialist_status_enum,
        server_default=text("'available'")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="specialist_profile")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="specialist")
    prescriptions: Mapped[list["Prescription"]] = relationship(back_populates="specialist")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="specialist")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True
    )
    specialist_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("specialist_profiles.id", ondelete="CASCADE"),
        index=True
    )
    scheduled_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(
        appointment_status_enum,
        server_default=text("'scheduled'")
    )
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    client: Mapped["ClientProfile"] = relationship(back_populates="appointments")
    specialist: Mapped["SpecialistProfile"] = relationship(back_populates="appointments")


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    test_type: Mapped[str] = mapped_column(test_type_enum, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    questions: Mapped[list["TestQuestion"]] = relationship(back_populates="test")
    results: Mapped[list["TestResult"]] = relationship(back_populates="test")


class TestQuestion(Base):
    __tablename__ = "test_questions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    test_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"),
        index=True
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_order: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    test: Mapped["Test"] = relationship(back_populates="questions")
    options: Mapped[list["TestOption"]] = relationship(back_populates="question")


class TestOption(Base):
    __tablename__ = "test_options"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("test_questions.id", ondelete="CASCADE"),
        index=True
    )
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    question: Mapped["TestQuestion"] = relationship(back_populates="options")


class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True
    )
    test_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"),
        index=True
    )
    answers: Mapped[Any] = mapped_column(JSONB, nullable=False)
    total_score: Mapped[float] = mapped_column(Float, nullable=False)
    interpretation: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    client: Mapped["ClientProfile"] = relationship(back_populates="test_results")
    test: Mapped["Test"] = relationship(back_populates="results")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True
    )
    specialist_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("specialist_profiles.id", ondelete="CASCADE"),
        index=True
    )
    medication_name: Mapped[str] = mapped_column(String(100), nullable=False)
    dosage: Mapped[str] = mapped_column(String(50), nullable=False)
    frequency: Mapped[str] = mapped_column(String(50), nullable=False)
    duration: Mapped[str] = mapped_column(String(50), nullable=False)
    instructions: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        prescription_status_enum,
        server_default=text("'active'")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    client: Mapped["ClientProfile"] = relationship(back_populates="prescriptions")
    specialist: Mapped["SpecialistProfile"] = relationship(back_populates="prescriptions")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True
    )
    specialist_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("specialist_profiles.id", ondelete="CASCADE"),
        nullable=True
    )
    recommendation_type: Mapped[str] = mapped_column(recommendation_type_enum, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    client: Mapped["ClientProfile"] = relationship(back_populates="recommendations")
    specialist: Mapped[Optional["SpecialistProfile"]] = relationship(back_populates="recommendations")

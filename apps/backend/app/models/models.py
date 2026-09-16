import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    Integer,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # admin, scientist, user
    created_at = Column(DateTime, default=datetime.utcnow)

    predictions = relationship(
        "PredictionHistory", back_populates="user", cascade="all, delete-orphan"
    )
    settings = relationship(
        "UserSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    sessions = relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan"
    )


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    refresh_token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")


class PredictionHistory(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    target_hex = Column(String(7), nullable=False)
    target_lab_l = Column(Float, nullable=False)
    target_lab_a = Column(Float, nullable=False)
    target_lab_b = Column(Float, nullable=False)
    base_colors_config = Column(JSONB, nullable=False)
    ml_predicted_ratios = Column(JSONB, nullable=False)
    optimized_ratios = Column(JSONB, nullable=False)
    delta_e = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="predictions")
    feedback = relationship(
        "Feedback",
        back_populates="prediction",
        uselist=False,
        cascade="all, delete-orphan",
    )


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    default_delta_e_threshold = Column(Float, default=1.0)
    optimizer_max_iterations = Column(Integer, default=1000)
    enable_explainability = Column(Boolean, default=True)

    user = relationship("User", back_populates="settings")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prediction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("predictions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    rating = Column(Integer, nullable=False)  # 1-5
    user_comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    prediction = relationship("PredictionHistory", back_populates="feedback")


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, index=True, nullable=False)  # formulate_run, chat_run
    metadata_info = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ApiLog(Base):
    __tablename__ = "api_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

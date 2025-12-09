"""
SQLAlchemy models for the consultation platform
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, Enum, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class UserRole(str, enum.Enum):
    """User roles in the system"""
    USER = "user"
    ASTROLOGER = "astrologer"
    MODERATOR = "moderator"
    ADMIN = "admin"


class QuestionStatus(str, enum.Enum):
    """Status of a question"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    ANSWERED = "answered"
    CLOSED = "closed"


class MessageType(str, enum.Enum):
    """Type of message"""
    QUESTION = "question"
    ANSWER = "answer"
    FOLLOW_UP = "follow_up"
    CLARIFICATION = "clarification"


class NotificationType(str, enum.Enum):
    """Type of notification"""
    QUESTION_RECEIVED = "question_received"
    ANSWER_PROVIDED = "answer_provided"
    FOLLOW_UP = "follow_up"
    NEW_CONSULTATION = "new_consultation"
    PAYMENT_CONFIRMED = "payment_confirmed"


class User(Base):
    """User model - represents both regular users and astrologers"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150))
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.USER)
    
    # Astrologer specific fields
    specialization = Column(String(200))  # e.g., "Vedic Astrology", "Love & Relationships"
    bio = Column(Text)
    experience_years = Column(Integer)
    hourly_rate = Column(Float, default=50.0)  # For future consultation fees
    average_rating = Column(Float, default=0.0)
    total_consultations = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    
    # Account status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    questions = relationship("Question", back_populates="user", foreign_keys="Question.user_id")
    answers = relationship("Message", back_populates="astrologer", foreign_keys="Message.astrologer_id")
    ratings = relationship("Rating", back_populates="astrologer", foreign_keys="Rating.astrologer_id")
    notifications = relationship("Notification", back_populates="user")
    consultations = relationship("Consultation", back_populates="user", foreign_keys="Consultation.user_id")


class Question(Base):
    """Represents a user's question submitted for astrologers"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String(100), index=True)  # Marriage, Work, Money, etc.
    title = Column(String(300), nullable=False)
    description = Column(Text)
    status = Column(Enum(QuestionStatus), default=QuestionStatus.PENDING, index=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)  # Assigned astrologer
    
    # Additional context
    birth_date = Column(DateTime)
    birth_place = Column(String(150))
    birth_time = Column(String(10))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    answered_at = Column(DateTime)
    
    # Priority and visibility
    is_public = Column(Boolean, default=False)  # Can be answered by any astrologer
    priority = Column(Integer, default=0)  # For sorting queue
    
    # Relationships
    user = relationship("User", back_populates="questions", foreign_keys=[user_id])
    messages = relationship("Message", back_populates="question", cascade="all, delete-orphan")
    consultation = relationship("Consultation", back_populates="question", uselist=False)


class Message(Base):
    """Represents messages in a question/answer thread"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # User sending the message
    astrologer_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # If sent by astrologer
    
    message_type = Column(Enum(MessageType), default=MessageType.QUESTION)
    content = Column(Text, nullable=False)
    
    # Message metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    edited_at = Column(DateTime)
    is_edited = Column(Boolean, default=False)
    
    # Relationships
    question = relationship("Question", back_populates="messages")
    astrologer = relationship("User", back_populates="answers", foreign_keys=[astrologer_id])


class Consultation(Base):
    """Represents a paid consultation"""
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    astrologer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Consultation details
    duration_minutes = Column(Integer, default=30)
    status = Column(String(50), default="scheduled")  # scheduled, ongoing, completed, cancelled
    amount = Column(Float, nullable=False)
    payment_id = Column(String(150), index=True)  # Reference to payment gateway
    
    # Scheduling
    scheduled_at = Column(DateTime)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    
    # Notes
    notes = Column(Text)
    recording_path = Column(String(255))  # Path to saved consultation recording
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="consultations", foreign_keys=[user_id])
    question = relationship("Question", back_populates="consultation")


class Rating(Base):
    """User ratings for astrologers"""
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    astrologer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    rating = Column(Integer, nullable=False)  # 1-5
    review = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    astrologer = relationship("User", back_populates="ratings", foreign_keys=[astrologer_id])


class Notification(Base):
    """System notifications for users"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    type = Column(Enum(NotificationType))
    subject = Column(String(200))
    message = Column(Text)
    related_question_id = Column(Integer, ForeignKey("questions.id"))
    
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")


class AstrologerQueue(Base):
    """Queue management for questions assignment"""
    __tablename__ = "astrologer_queue"

    id = Column(Integer, primary_key=True, index=True)
    astrologer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    
    # Queue position
    position = Column(Integer)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    expected_completion = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    
    # Relationships
    astrologer = relationship("User")
    question = relationship("Question")


class SystemLog(Base):
    """System activity logs for auditing"""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100))
    details = Column(JSON)
    status_code = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

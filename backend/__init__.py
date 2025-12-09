"""
Backend package initialization
"""

from backend.database import Base, engine, SessionLocal, get_db, init_db
from backend.models import (
    User, Question, Message, Consultation, Rating,
    Notification, UserRole, QuestionStatus, MessageType, NotificationType
)

__version__ = "1.0.0"
__author__ = "Cosmos Astrology Team"

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    "User",
    "Question",
    "Message",
    "Consultation",
    "Rating",
    "Notification",
    "UserRole",
    "QuestionStatus",
    "MessageType",
    "NotificationType",
]

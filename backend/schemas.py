"""
Pydantic schemas for request/response validation
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=100)
    email: str
    full_name: Optional[str] = None


class UserRegister(UserBase):
    """User registration schema"""
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """User login schema"""
    username: str
    password: str


class AstrologerProfile(UserBase):
    """Astrologer profile schema"""
    specialization: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    hourly_rate: Optional[float] = 50.0


class UserResponse(UserBase):
    """User response schema"""
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class AstrologerResponse(UserResponse):
    """Astrologer response schema"""
    specialization: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    average_rating: float
    total_consultations: int


# Question Schemas
class QuestionCreate(BaseModel):
    """Create question schema"""
    category: str = Field(..., min_length=1)
    title: str = Field(..., min_length=10, max_length=300)
    description: Optional[str] = None
    birth_date: Optional[datetime] = None
    birth_place: Optional[str] = None
    birth_time: Optional[str] = None
    is_public: bool = False


class QuestionUpdate(BaseModel):
    """Update question schema"""
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    priority: Optional[int] = None


class QuestionResponse(BaseModel):
    """Question response schema"""
    id: int
    user_id: int
    category: str
    title: str
    description: Optional[str]
    status: str
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime
    answered_at: Optional[datetime]
    is_public: bool
    
    class Config:
        from_attributes = True


class QuestionDetailResponse(QuestionResponse):
    """Detailed question response with messages"""
    user: UserResponse
    messages: List['MessageResponse'] = []


# Message Schemas
class MessageCreate(BaseModel):
    """Create message schema"""
    content: str = Field(..., min_length=5)
    message_type: str = "question"


class MessageResponse(BaseModel):
    """Message response schema"""
    id: int
    question_id: int
    user_id: int
    astrologer_id: Optional[int]
    content: str
    message_type: str
    created_at: datetime
    is_edited: bool
    
    class Config:
        from_attributes = True


# Consultation Schemas
class ConsultationCreate(BaseModel):
    """Create consultation schema"""
    question_id: Optional[int] = None
    astrologer_id: int
    duration_minutes: int = 30
    amount: float
    scheduled_at: Optional[datetime] = None


class ConsultationResponse(BaseModel):
    """Consultation response schema"""
    id: int
    user_id: int
    astrologer_id: int
    status: str
    amount: float
    duration_minutes: int
    scheduled_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Rating Schemas
class RatingCreate(BaseModel):
    """Create rating schema"""
    astrologer_id: int
    question_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = None


class RatingResponse(BaseModel):
    """Rating response schema"""
    id: int
    user_id: int
    astrologer_id: int
    rating: int
    review: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Notification Schemas
class NotificationResponse(BaseModel):
    """Notification response schema"""
    id: int
    type: str
    subject: str
    message: str
    is_read: bool
    created_at: datetime
    related_question_id: Optional[int]
    
    class Config:
        from_attributes = True


# Search and Filter Schemas
class QuestionFilter(BaseModel):
    """Question filter schema"""
    category: Optional[str] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None
    assigned_to: Optional[int] = None
    skip: int = 0
    limit: int = 20


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    total: int
    skip: int
    limit: int
    items: List[dict]

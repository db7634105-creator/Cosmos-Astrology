"""
Main FastAPI application - Astrology Consultation Platform Backend
"""

import os
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.database import Base, engine, get_db, init_db
from backend.models import User, Question, Message, Notification, UserRole, QuestionStatus, MessageType, NotificationType
from backend.auth import get_password_hash, verify_password, verify_token, get_tokens
from backend.schemas import (
    UserRegister, UserLogin, UserResponse, QuestionCreate, QuestionResponse, 
    QuestionDetailResponse, MessageCreate, MessageResponse, NotificationResponse,
    AstrologerResponse, ConsultationResponse, RatingResponse
)
from backend.websocket_manager import manager

# Initialize FastAPI app
app = FastAPI(
    title="Astrology Consultation Platform",
    description="Real-time consultation platform connecting users with astrologers",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security - Simple Bearer token authentication


# ==================== Startup Events ====================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("Initializing database...")
    init_db()
    print("Database ready!")


# ==================== Utility Functions ====================

async def get_current_user(authorization: str = None, db: Session = Depends(get_db)) -> User:
    """Get current authenticated user from JWT token"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = parts[1]
    token_data = verify_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


async def get_current_astrologer(current_user: User = Depends(get_current_user)) -> User:
    """Ensure current user is an astrologer"""
    if current_user.role not in [UserRole.ASTROLOGER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only astrologers can access this endpoint"
        )
    return current_user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Ensure current user is an admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this endpoint"
        )
    return current_user


# ==================== Authentication Endpoints ====================

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=get_password_hash(user_data.password),
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.post("/api/auth/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT tokens"""
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    tokens = get_tokens(user.id, user.username, user.role.value)
    return {
        **tokens.dict(),
        "user": UserResponse.from_orm(user)
    }


# ==================== User Endpoints ====================

@app.get("/api/users/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/api/astrologers", response_model=list[AstrologerResponse])
async def list_astrologers(
    skip: int = 0,
    limit: int = 20,
    specialization: str = None,
    db: Session = Depends(get_db)
):
    """List available astrologers"""
    query = db.query(User).filter(
        User.role == UserRole.ASTROLOGER,
        User.is_active == True,
        User.is_verified == True
    )
    
    if specialization:
        query = query.filter(User.specialization.contains(specialization))
    
    astrologers = query.offset(skip).limit(limit).all()
    return astrologers


# ==================== Question Endpoints ====================

@app.post("/api/questions", response_model=QuestionResponse)
async def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new question"""
    new_question = Question(
        user_id=current_user.id,
        category=question_data.category,
        title=question_data.title,
        description=question_data.description,
        birth_date=question_data.birth_date,
        birth_place=question_data.birth_place,
        birth_time=question_data.birth_time,
        is_public=question_data.is_public,
        status=QuestionStatus.PENDING,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    # Notify astrologers if public question
    if question_data.is_public:
        # TODO: Send notification to all astrologers
        pass
    
    return new_question


@app.get("/api/questions/{question_id}", response_model=QuestionDetailResponse)
async def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get question details with all messages"""
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check authorization
    if question.user_id != current_user.id and current_user.role not in [UserRole.ASTROLOGER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to view this question")
    
    return question


@app.get("/api/questions")
async def list_user_questions(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """List user's questions"""
    query = db.query(Question).filter(Question.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Question.status == status_filter)
    
    total = query.count()
    questions = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": questions
    }


@app.get("/api/astrologer/queue")
async def get_astrologer_queue(
    current_user: User = Depends(get_current_astrologer),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get questions assigned to astrologer"""
    questions = db.query(Question).filter(
        Question.assigned_to == current_user.id,
        Question.status != QuestionStatus.CLOSED
    ).offset(skip).limit(limit).all()
    
    total = db.query(Question).filter(
        Question.assigned_to == current_user.id,
        Question.status != QuestionStatus.CLOSED
    ).count()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": questions
    }


# ==================== Message Endpoints ====================

@app.post("/api/questions/{question_id}/messages", response_model=MessageResponse)
async def send_message(
    question_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in a question thread"""
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check authorization
    if question.user_id != current_user.id and question.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to message this question")
    
    # Create message
    new_message = Message(
        question_id=question_id,
        user_id=current_user.id,
        astrologer_id=current_user.id if current_user.role in [UserRole.ASTROLOGER, UserRole.MODERATOR] else None,
        message_type=MessageType.ANSWER if current_user.id == question.assigned_to else MessageType.FOLLOW_UP,
        content=message_data.content,
        created_at=datetime.utcnow()
    )
    
    db.add(new_message)
    
    # Update question status if answer provided
    if current_user.id == question.assigned_to and message_data.message_type == "answer":
        question.status = QuestionStatus.ANSWERED
        question.answered_at = datetime.utcnow()
    
    db.commit()
    db.refresh(new_message)
    
    # Broadcast via WebSocket
    await manager.broadcast_to_question(
        question_id,
        {
            "type": "new_message",
            "message": MessageResponse.from_orm(new_message).dict()
        }
    )
    
    return new_message


# ==================== Notification Endpoints ====================

@app.get("/api/notifications", response_model=list[NotificationResponse])
async def get_notifications(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
    unread_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    total = query.count()
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    return notifications


@app.patch("/api/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    
    return {"status": "success"}


# ==================== WebSocket Endpoints ====================

@app.websocket("/ws/questions/{question_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    question_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time messaging"""
    # Verify question and user exist
    question = db.query(Question).filter(Question.id == question_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not question or not user:
        await websocket.close(code=4004)
        return
    
    # Check authorization
    if question.user_id != user_id and question.assigned_to != user_id:
        await websocket.close(code=4003)
        return
    
    await manager.connect(websocket, question_id, user_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process received message
            if data.get("type") == "message":
                message_content = data.get("content")
                
                # Save to database
                new_message = Message(
                    question_id=question_id,
                    user_id=user_id,
                    astrologer_id=user_id if question.assigned_to == user_id else None,
                    message_type=MessageType.ANSWER if question.assigned_to == user_id else MessageType.FOLLOW_UP,
                    content=message_content,
                    created_at=datetime.utcnow()
                )
                
                db.add(new_message)
                db.commit()
                
                # Broadcast to all connected users
                await manager.broadcast_to_question(
                    question_id,
                    {
                        "type": "message",
                        "user_id": user_id,
                        "username": user.username,
                        "content": message_content,
                        "message_id": new_message.id
                    }
                )
    
    except WebSocketDisconnect:
        manager.disconnect(question_id, user_id)
        await manager.broadcast_to_question(
            question_id,
            {"type": "user_disconnected", "user_id": user_id}
        )


# ==================== Health Check ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "connections": manager.get_connection_count()
    }


# ==================== Root ====================

@app.get("/frontend/dashboard/")
async def dashboard():
    """Serve dashboard HTML"""
    return FileResponse("frontend/dashboard/index.html", media_type="text/html")

@app.get("/")
async def root():
    """Root endpoint - serve main app"""
    return FileResponse("frontend/index.html", media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Database configuration and session management
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# Database URL - use SQLite for simplicity, easily switchable to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./astrology_consultation.db")

# Create engine with proper configuration
if "sqlite" in DATABASE_URL:
    # For SQLite, we need special configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=os.getenv("SQL_ECHO", "False").lower() == "true"
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # PostgreSQL or other database
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("SQL_ECHO", "False").lower() == "true",
        pool_pre_ping=True
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
    
    # Create demo user if doesn't exist
    from backend.models import User, UserRole
    from backend.auth import get_password_hash
    
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == "demo").first()
        if not existing_user:
            demo_user = User(
                username="demo",
                email="demo@example.com",
                password_hash=get_password_hash("demo123"),
                full_name="Demo User",
                role=UserRole.USER,
                is_active=True
            )
            db.add(demo_user)
            db.commit()
            print("✅ Demo user created: username=demo, password=demo123")
    except Exception as e:
        print(f"Demo user creation skipped: {e}")
        db.rollback()
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine - this is the actual connection to PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # Check connection is alive before using
    pool_size=10,            # Max 10 connections at once
    max_overflow=20          # Allow 20 extra connections if needed
)

# SessionLocal - each request gets its own database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base - all our database models will inherit from this
Base = declarative_base()

# Dependency - used in FastAPI routes to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
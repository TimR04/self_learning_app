"""
This module initializes the database connection for the self-learning application.
It sets up the SQLite database using SQLAlchemy and provides session management functions.

All functions follow PEP8 style guidelines and ensure proper handling of database connections.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL (change this if using a different database)
SQLALCHEMY_DATABASE_URL = "sqlite:///./self_learning_app.db"

# SQLAlchemy database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session local class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class to define database models
Base = declarative_base()

def get_db():
    """
    Provides a new database session for each request.
    
    Yields:
        Session: A SQLAlchemy session that can be used for database interactions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initializes the database by creating tables if they do not exist.
    Calls the metadata create_all method to apply the table schemas.
    """
    from .models import User, Book  # Importing models here to avoid circular imports
    Base.metadata.create_all(bind=engine)

"""
This module handles database connection and initialization for the self-learning application.
It sets up the SQLAlchemy engine, session management, and initializes the database schema.

All functions follow PEP8 style guidelines and ensure proper handling of database connections.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL (adjust if using a different database like PostgreSQL or MySQL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./self_learning_app.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models to inherit from
Base = declarative_base()

def get_db():
    """
    Provides a new database session for each request.
    
    Yields:
        db (Session): A SQLAlchemy session to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initializes the database by creating tables if they don't exist.
    Calls the metadata create_all method to apply the table schema.
    """
    from .models import User, Book  # Import models to avoid circular imports
    Base.metadata.create_all(bind=engine)

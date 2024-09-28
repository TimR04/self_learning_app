from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Import the Base from database

class User(Base):
    """
    User model representing the user of the application.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(String, nullable=False)

    # Relationship to the books owned by the user
    books = relationship("Book", back_populates="owner")


class Book(Base):
    """
    Book model representing books that belong to users.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pages_read = Column(Integer, default=0)
    is_favorite = Column(Integer, default=False)

    # Relationship to the user who owns this book
    owner = relationship("User", back_populates="books")

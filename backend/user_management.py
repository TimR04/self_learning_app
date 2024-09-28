"""
This module handles user profile management for the self-learning application.
It includes routes for retrieving and updating user profile information, ensuring GDPR compliance.

All routes follow PEP8 style guidelines and secure handling of user data.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from backend.database.models import User
from .auth import get_current_user  # To ensure only authenticated users can access profile information

# Create the FastAPI router for user profile management routes
user_management_routes = APIRouter()

@user_management_routes.get("/profile")
def get_user_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves the profile information for the authenticated user.

    Args:
        db (Session): The database session dependency.
        current_user (User): The currently authenticated user, fetched via JWT.

    Returns:
        dict: A dictionary containing the user's profile information.
    """
    return {
        "username": current_user.username,
        "email": current_user.email,  # Assuming email is stored in the User model
        "created_at": current_user.created_at,  # When the user was created
    }

@user_management_routes.put("/profile")
def update_user_profile(username: str = None, email: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Updates the user's profile information, including username and email.

    Args:
        username (str, optional): The new username to update.
        email (str, optional): The new email to update.
        db (Session): The database session dependency.
        current_user (User): The currently authenticated user.

    Returns:
        dict: A success message indicating the profile was updated.
    """
    if username:
        current_user.username = username
    if email:
        current_user.email = email

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated successfully."}

@user_management_routes.delete("/profile")
def delete_user_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Deletes the current user's profile and all associated data.

    Args:
        db (Session): The database session dependency.
        current_user (User): The currently authenticated user.

    Returns:
        dict: A success message indicating the user profile was deleted.
    """
    db.delete(current_user)
    db.commit()

    return {"message": "User profile deleted successfully."}

"""
This module handles user authentication for the self-learning application.
It includes routes for user registration, login, and token management, using JSON Web Tokens (JWT) for secure authentication.

All routes follow PEP8 style guidelines and adhere to GDPR compliance for secure handling of user data.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from .database import get_db
from backend.database.models import User

# Create the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret key and algorithm
SECRET_KEY = "your-secret-key-here"  # Hard-coded secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create the FastAPI router for authentication routes
auth_routes = APIRouter()

def get_password_hash(password: str):
    """
    Hashes the provided password using bcrypt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """
    Verifies that the provided plain-text password matches the hashed password.

    Args:
        plain_password (str): The plain-text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """
    Creates a JWT access token for the user.

    Args:
        data (dict): The data to include in the token's payload.

    Returns:
        str: The JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import APIRouter

# Initialize the router
auth_routes = APIRouter()

# Example route
@auth_routes.post("/register")
def register_user(username: str, password: str):
    """
    This is a sample route for user registration.
    In reality, you'd handle registration logic here.
    """
    return {"message": f"User {username} registered successfully!"}

@auth_routes.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    """
    Authenticates a user by verifying their password and returning a JWT token.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.
        db (Session): The database session dependency.

    Returns:
        dict: A JWT token for the authenticated user.
    """
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verify_password(password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_routes.get("/me")
def get_current_user(token: str):
    """
    Retrieves the current user's data based on the provided JWT token.

    Args:
        token (str): The JWT token from the authorization header.

    Returns:
        dict: The user's data extracted from the token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

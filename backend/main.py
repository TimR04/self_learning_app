"""
This is the main entry point for the backend of the self-learning application.
It includes routes for user authentication, book management, and handles initialization tasks like database setup.
"""

from fastapi import FastAPI
from .database import init_db
from .auth import auth_routes
from .books import books_routes

# Initialize the FastAPI application
app = FastAPI()  # Ensure this line is present and correct

# Event triggered on startup to initialize the database
@app.on_event("startup")
def startup_event():
    init_db()

# Include authentication routes from the auth module
app.include_router(auth_routes, prefix="/auth")

# Include book management routes from the books module
app.include_router(books_routes, prefix="/books")

# A simple test route to confirm the app is running
@app.get("/")
def read_root():
    return {"message": "Welcome to the Self-Learning App API!"}

"""
This is the initialization file for the backend module of the self-learning application.

It sets up the FastAPI application, initializes the database connections, and imports the necessary routes for user authentication, book management, and other backend functionalities.

All functions and modules follow PEP8 style guidelines.
"""

from fastapi import FastAPI
from .database import init_db
from .auth import auth_routes
from .books import books_routes

# Initialize the FastAPI app
app = FastAPI()

# Initialize the database (ensure tables are created if they don't exist)
@app.on_event("startup")
def startup_event():
    """
    Event triggered at the startup of the FastAPI application.
    Ensures the database is initialized and ready for requests.
    """
    init_db()

# Include the authentication and book management routes
app.include_router(auth_routes, prefix="/auth")
app.include_router(books_routes, prefix="/books")


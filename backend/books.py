"""
This module handles the book-related functionality for the self-learning application.
It includes routes for searching books by genre, marking books as read, and managing favorites.

All routes follow PEP8 style guidelines and adhere to GDPR compliance for secure handling of user data.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .database.models import User, Book  # Corrected Import
from .auth import get_current_user  # Assuming you have this function to get the current user
import requests

# Create the FastAPI router for book-related routes
books_routes = APIRouter()

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books_api(keyword: str):
    """
    Queries the Google Books API for books related to a specific keyword (genre or topic).
    
    Args:
        keyword (str): The search keyword (e.g., genre or topic).
    
    Returns:
        list: A list of books (with title, author, and description) matching the search criteria.
    """
    response = requests.get(f"{GOOGLE_BOOKS_API_URL}?q={keyword}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Google Books API.")
    
    books_data = response.json().get("items", [])
    return [
        {
            "id": book["id"],
            "title": book["volumeInfo"].get("title", "No title available"),
            "author": ", ".join(book["volumeInfo"].get("authors", ["Unknown author"])),
            "description": book["volumeInfo"].get("description", "No description available")
        }
        for book in books_data
    ]

@books_routes.get("/search_books/{genre}")
def search_books(genre: str, db: Session = Depends(get_db)):
    """
    Searches for books based on a genre and returns a list of recommended books.
    
    Args:
        genre (str): The selected genre for book recommendations.
        db (Session): The database session dependency.
    
    Returns:
        dict: A dictionary containing the list of recommended books.
    """
    try:
        books = search_books_api(genre)
        return {"books": books}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@books_routes.post("/add_book")
def add_book_to_user(book_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):  # Corrected user dependency
    """
    Adds a selected book to the user's book list.
    
    Args:
        book_id (str): The ID of the selected book.
        db (Session): The database session dependency.
        user (User): The authenticated user.
    
    Returns:
        dict: A success message indicating the book was added to the user's list.
    """
    # Fetch the book details from Google Books API
    book_data = search_books_api(book_id)[0]  # Assuming the book is unique
    
    # Add the book to the user's list
    new_book = Book(title=book_data["title"], author=book_data["author"], user_id=user.id, description=book_data["description"])
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {"message": f"Book '{book_data['title']}' added to your list."}

@books_routes.post("/mark_read")
def mark_book_as_read(book_id: str, pages_read: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):  # Corrected user dependency
    """
    Marks a book as read by the user and stores the progress.
    
    Args:
        book_id (str): The ID of the book to mark as read.
        pages_read (int): The number of pages read by the user.
        db (Session): The database session dependency.
        user (User): The authenticated user.
    
    Returns:
        dict: A success message indicating the book was marked as read.
    """
    # Find the book in the user's list
    book = db.query(Book).filter(Book.id == book_id, Book.user_id == user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found in your list.")
    
    # Update the book's read status and progress
    book.pages_read = pages_read
    db.commit()

    return {"message": f"Book '{book.title}' marked as read. You have read {pages_read} pages."}

@books_routes.post("/add_favorite")
def add_book_to_favorites(book_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):  # Corrected user dependency
    """
    Adds a selected book to the user's list of favorite books.
    
    Args:
        book_id (str): The ID of the selected book.
        db (Session): The database session dependency.
        user (User): The authenticated user.
    
    Returns:
        dict: A success message indicating the book was added to favorites.
    """
    # Find the book in the user's list
    book = db.query(Book).filter(Book.id == book_id, Book.user_id == user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found in your list.")
    
    # Mark the book as a favorite
    book.is_favorite = True
    db.commit()

    return {"message": f"Book '{book.title}' added to your favorites."}

@books_routes.post("/remove_favorite")
def remove_book_from_favorites(book_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):  # Corrected user dependency
    """
    Removes a book from the user's list of favorite books.
    
    Args:
        book_id (str): The ID of the selected book.
        db (Session): The database session dependency.
        user (User): The authenticated user.
    
    Returns:
        dict: A success message indicating the book was removed from favorites.
    """
    # Find the book in the user's list
    book = db.query(Book).filter(Book.id == book_id, Book.user_id == user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found in your list.")
    
    # Remove the book from favorites
    book.is_favorite = False
    db.commit()

    return {"message": f"Book '{book.title}' removed from your favorites."}

@books_routes.get("/my_books")
def get_my_books(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Fetch the books for the currently authenticated user.
    """
    # Use the ID of the currently logged-in user from the JWT token or session
    user_id = current_user["id"]

    # Query the books table to get books for the authenticated user
    books = db.query(Book).filter_by(user_id=user_id).all()

    return {"books": books}

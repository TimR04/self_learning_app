import requests
import PySimpleGUI as sg

# Define the API base URL (adjust as necessary)
API_BASE_URL = "http://127.0.0.1:8000"

def handle_genre_selection(genre):
    # Fetch books by genre
    response = requests.get(f"{API_BASE_URL}/books/search_books/{genre}")
    if response.status_code == 200:
        books = response.json().get("books", [])
        return books
    else:
        sg.popup("Error: Could not fetch books.")
        return []

def view_my_books():
    """
    Fetch the books that the user has added or marked as favorites.
    Communicates with the FastAPI backend.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/books/my_books")
        if response.status_code == 200:
            books = response.json().get("books", [])
            return books
        else:
            sg.popup("Error: Could not fetch your books from the backend.")
            return []
    except requests.RequestException as e:
        sg.popup(f"An error occurred while fetching your books: {e}")
        return []

def handle_book_selection(book_id):
    sg.popup(f"Book {book_id} selected")

def mark_book_as_read(book_id, pages_read):
    response = requests.post(f"{API_BASE_URL}/books/mark_read", json={"book_id": book_id, "pages_read": pages_read})
    if response.status_code == 200:
        sg.popup(f"Book marked as read. Pages read: {pages_read}")
    else:
        sg.popup("Error: Could not mark the book as read.")

def add_book_to_favorites(book_id):
    response = requests.post(f"{API_BASE_URL}/books/add_favorite", json={"book_id": book_id})
    if response.status_code == 200:
        sg.popup(f"Book added to favorites.")
    else:
        sg.popup("Error: Could not add book to favorites.")

def remove_book_from_favorites(book_id):
    response = requests.post(f"{API_BASE_URL}/books/remove_favorite", json={"book_id": book_id})
    if response.status_code == 200:
        sg.popup(f"Book removed from favorites.")
    else:
        sg.popup("Error: Could not remove book from favorites.")

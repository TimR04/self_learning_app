import PySimpleGUI as sg
from button_handlers import handle_genre_selection, handle_book_selection, mark_book_as_read, add_book_to_favorites, remove_book_from_favorites, view_my_books

# Define the layout of the user interface
layout = [
    [sg.Text("Select a Genre for Book Recommendations:")],
    [sg.Button("Science Fiction"), sg.Button("Mystery"), sg.Button("Fantasy")],
    [sg.Button("View My Books")],  # New button for viewing user's books
    [sg.Button("Exit")]
]

# Create the window
window = sg.Window("Book Search", layout)

def show_book_options(book_id, book_title):
    """
    Display additional options for the selected book (mark as read, add to favorites, etc.).
    """
    book_options_layout = [
        [sg.Text(f"Selected Book: {book_title}")],
        [sg.Button("Mark as Read"), sg.Button("Add to Favorites"), sg.Button("Remove from Favorites")],
        [sg.Button("Back to Genre Selection")]
    ]
    
    book_options_window = sg.Window("Book Options", book_options_layout)
    
    while True:
        event, _ = book_options_window.read()
        
        if event == sg.WINDOW_CLOSED or event == "Back to Genre Selection":
            break
        elif event == "Mark as Read":
            pages_read = sg.popup_get_text("Enter the number of pages read:", "Mark as Read")
            if pages_read:
                mark_book_as_read(book_id, pages_read)
        elif event == "Add to Favorites":
            add_book_to_favorites(book_id)
        elif event == "Remove from Favorites":
            remove_book_from_favorites(book_id)
    
    book_options_window.close()

# Main event loop to process user input
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event in ["Science Fiction", "Mystery", "Fantasy"]:
        books = handle_genre_selection(event)
        
        if books:
            book_titles = [f"{book['title']} by {book['author']}" for book in books]
            selected_book = sg.popup_get_text("Select a book from the list:\n" + "\n".join(book_titles), "Select a Book")
            
            if selected_book:
                for book in books:
                    if f"{book['title']} by {book['author']}" == selected_book:
                        book_id = book['id']
                        show_book_options(book_id, selected_book)
                        break
        else:
            sg.popup(f"No books found for {event}.")
    
    # Handle "View My Books" button
    elif event == "View My Books":
        my_books = view_my_books()  # Fetch books from the backend
        if my_books:
            book_list = "\n".join([f"{book['title']} by {book['author']}" for book in my_books])
            sg.popup(f"My Books:\n\n{book_list}")
        else:
            sg.popup("No books found in your collection.")

# Close the window
window.close()

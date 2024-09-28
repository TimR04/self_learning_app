"""
This module handles the logic for branching questions in the self-learning application.
It manages user input and dynamically determines the next steps or questions based on their choices.

Communication between the frontend and backend is handled via a custom API.
All functions follow PEP8 style guidelines, and user data is handled securely, adhering to GDPR compliance.
"""

from button_handlers import handle_genre_selection

# Global variable to store user session data
TOKEN = None

def handle_branching_question(user_input: str, token: str):
    """
    Handles the logic for determining the next question or step based on the user's input.

    Args:
        user_input (str): The user's selection or answer to the current question.
        token (str): The user's authentication token.

    Returns:
        dict: The next question or action, based on the user's input.
    """
    global TOKEN
    TOKEN = token
    
    if user_input in ['Science Fiction', 'Fantasy', 'Mystery', 'Non-fiction']:
        # If user selects a genre, fetch book recommendations based on the selection
        return get_book_recommendations(user_input)
    else:
        # Handle other inputs or branching logic if necessary
        return {"message": "No further branching logic implemented."}


def get_book_recommendations(genre: str):
    """
    Fetches book recommendations based on the user's selected genre.

    Args:
        genre (str): The selected genre for book recommendations.

    Returns:
        dict: A dictionary containing book recommendations fetched from the backend.
    """
    response = handle_genre_selection(genre, TOKEN)
    if 'books' in response:
        return {
            "message": f"Recommendations for {genre}",
            "books": response['books']
        }
    else:
        return {
            "message": f"Failed to fetch recommendations for {genre}. Error: {response.get('error', 'Unknown error')}"
        }


def process_user_input(user_input: str, token: str):
    """
    Processes the user's input, handles branching questions, and fetches the necessary data.

    Args:
        user_input (str): The user's selection or input.
        token (str): The user's authentication token.

    Returns:
        dict: The response or next action based on the processed input.
    """
    return handle_branching_question(user_input, token)


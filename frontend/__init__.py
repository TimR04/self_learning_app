"""
This is the initialization file for the frontend module of the self-learning application.

The frontend communicates with the backend through a custom API and interacts with the SQLite database.
User profiles are handled with secure password storage, registration, and GDPR compliance.
The frontend is implemented using PySimpleGUI for a simple user interface.
"""

# Import necessary modules for frontend operation
import PySimpleGUI as sg
import requests
import json

# API configuration (adjust as needed)
API_BASE_URL = "http://127.0.0.1:8000"

# Function to send requests to the backend for user authentication and registration

def register_user(username: str, password: str):
    """
    Registers a new user by sending a POST request to the backend.
    
    Args:
        username (str): The desired username for the new account.
        password (str): The password for the new account.
    
    Returns:
        dict: The server's response as a dictionary containing status and possible error messages.
    """
    url = f"{API_BASE_URL}/register"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def login_user(username: str, password: str):
    """
    Logs in an existing user by sending a POST request to the backend.
    
    Args:
        username (str): The username for the account.
        password (str): The password for the account.
    
    Returns:
        dict: The server's response containing the authentication token and status.
    """
    url = f"{API_BASE_URL}/login"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_user_data(token: str):
    """
    Fetches user profile data from the backend by sending a GET request with authentication.
    
    Args:
        token (str): The authentication token for the logged-in user.
    
    Returns:
        dict: The server's response containing user profile information.
    """
    url = f"{API_BASE_URL}/user_profile"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

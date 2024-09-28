import PySimpleGUI as sg

layout = [
    [sg.Text("Please login")],
    [sg.Text("Username"), sg.Input(key="username")],
    [sg.Text("Password"), sg.Input(key="password", password_char="*")],
    [sg.Button("Login"), sg.Button("Cancel")]
]

window = sg.Window("Login", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Cancel":
        break
    elif event == "Login":
        username = values["username"]
        password = values["password"]
        # Call backend API to login (no code displayed to the user)
        print(f"Logging in user: {username}")  # This is just for debugging; can be removed

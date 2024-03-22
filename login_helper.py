#!/usr/bin/env python3
import tkinter as tk

def get_user_credentials():
    def login():
        nonlocal username
        nonlocal password
        username = username_entry.get()
        password = password_entry.get()
        login_window.destroy()

    # Initialize variables to hold username and password
    username = None
    password = None

    # Create the login window
    login_window = tk.Tk()
    login_window.title("Login")

    # Username entry
    tk.Label(login_window, text="Username:").grid(row=0, column=0, sticky="w")
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1)

    # Password entry
    tk.Label(login_window, text="Password:").grid(row=1, column=0, sticky="w")
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    # Login button
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.grid(row=2, columnspan=2)

    # Start the Tkinter event loop
    login_window.mainloop()

    # Return the username and password
    return username, password

if __name__ == "__main__":
    # If this script is executed directly, run the login window
    get_user_credentials()

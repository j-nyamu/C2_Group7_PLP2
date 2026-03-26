#!/usr/bin/env python3
"""
auth.py - Register and login for KultureKonnect.

Credentials are stored in the MySQL `users` table.
Passwords are hashed with SHA-256 + a per-user salt so they are
never stored in plain text.

using the colorama ui functions swaps the print to ui.info, ui.error, ui.success, etc. for better formatting and colour.
"""

import hashlib
import secrets
import mysql.connector
import time
from db import get_connection
import ui

# -- Internal helpers ----------------------------------------------------------


def _hash_password(password, salt=None):
    """
    Return (salt, hashed_password).
    If no salt is supplied a new random one is generated.
    """
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt, hashed


def _get_username():
    """Prompt for a non-empty, lowercase, alphanumeric username."""
    while True:
        username = input(ui.Fore.YELLOW + "  ▶  Username: " + ui.RESET).strip().lower()
        if not username:
             ui.error("Please enter a username. This field cannot be left blank.")
        elif not username.replace("_", "").isalnum():
            ui.error("Usernames may only contain letters, numbers, and underscores.")
        else:
            return username


def _get_password(confirm=False):
    """Prompt for a password (min 6 chars). If confirm=True ask twice."""
    while True:
        password = input(ui.Fore.YELLOW + "  ▶  Password: " + ui.RESET).strip()
        if len(password) < 6:
            ui.error("Your password is too short. Please use at least 6 characters.")
            continue
        if confirm:
            password2 = input(ui.Fore.YELLOW + "  ▶  Confirm password: " + ui.RESET).strip()
            if password != password2:
                ui.error("The passwords you entered do not match. Please try again.")
                continue
        return password


# -- Public: get user id for a given username ----------------------------------


def get_user_id(username):
    """Return the integer id for this username from the users table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None


# -- Public: register ---------------------------------------------------------


def register():
    """
    Walk the user through creating an account.
    Returns the new username on success, or None if they cancel.
    """
    ui.register_screen()

    while True:
        username = _get_username()
        if username == "back":
            return None

        # Check for duplicate by attempting INSERT and catching IntegrityError
        password = _get_password(confirm=True)
        if password.lower() == "back":
            return None

        salt, hashed = _hash_password(password)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, salt, password) VALUES (%s, %s, %s)",
                (username, salt, hashed),
            )
            conn.commit()
            cursor.close()
            conn.close()
            ui.success(
                f"  Your account has been created successfully! You can now log in as '{username}'."
            )
            return username
        except mysql.connector.errors.IntegrityError:
            ui.error(f"The username '{username}' is already taken. Please choose another.")
        except Exception as e:
            ui.error(f"  ERROR: Could not create account: {e}")
            return None


# -- Public: login ------------------------------------------------------------


def login():
    """
    Ask for username + password.
    Returns the username on success, or None after 3 failed attempts.
    """
    ui.login_screen()

    MAX_ATTEMPTS = 3

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(ui.DIM + f"\n  Attempt {attempt} of {MAX_ATTEMPTS}")
        username = input(ui.Fore.YELLOW + "  ▶  Username: " + ui.RESET).strip().lower()
        password = input(ui.Fore.YELLOW + "  ▶  Password: " + ui.RESET).strip()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT salt, password FROM users WHERE username = %s", (username,)
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            ui.error(f"  ERROR: Could not reach database: {e}")
            return None

        if not row:
            ui.error(
                "  We could not find an account with that username. Please check and try again."
            )
            continue

        salt, stored_hash = row
        _, hashed = _hash_password(password, salt)

        if hashed == stored_hash:
            ui.success(f"\n Login Successful!  Loading your session. Please wait . . .")
            time.sleep(3)
            
            return username
        else:
            remaining = MAX_ATTEMPTS - attempt
            if remaining > 0:
                ui.warn(
                    f"  That password is incorrect. You have {remaining} attempt(s) remaining."
                )
            else:
                ui.error(
                    "  You have used all your login attempts. Please return to the main menu and try again."
                )

    return None


# -- Public: auth gate --------------------------------------------------------


def auth_gate():
    """
    Show the opening menu and return a logged-in username,
    or None if the user chooses to exit.
    """
    ui.welcome_screen()
    while True:
        ui.auth_menu()

        choice = input(ui.Fore.YELLOW + "  ▶  Choose an option (1-3): " + ui.RESET).strip()

        if choice == "1":
            username = login()
            if username:
                return username

        elif choice == "2":
            username = register()
            if username:
                ui.info("Great! Please log in with your new account to continue.")
                username = login()
                if username:
                    return username

        elif choice == "3":
            ui.goodbye()
            return None

        else:
            ui.error("  That is not a valid option. Please enter 1, 2, or 3.")

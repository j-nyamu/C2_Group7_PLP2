#!/usr/bin/env python3
"""
auth.py - Register and login for KultureKonnect.

Each user gets:
  - An entry in users.json  (username + hashed password)
  - Their own profile file  profiles/<username>.json

Passwords are hashed with SHA-256 + a per-user salt so they are
never stored in plain text.
"""

import json
import os
import hashlib
import secrets

USERS_FILE   = "users.json"
PROFILES_DIR = "profiles"


# -- Internal helpers ----------------------------------------------------------

def _ensure_dirs():
    """Make sure the profiles/ folder exists."""
    os.makedirs(PROFILES_DIR, exist_ok=True)


def _load_users():
    """Return the users dict, or {} if the file is missing / corrupted."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_users(users):
    """Write the users dict back to disk."""
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except OSError as e:
        print(f"  ERROR: Could not save user data: {e}")


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
        username = input("  Username: ").strip().lower()
        if not username:
            print("  Please enter a username. This field cannot be left blank.")
        elif not username.replace("_", "").isalnum():
            print("  Usernames may only contain letters, numbers, and underscores.")
        else:
            return username


def _get_password(confirm=False):
    """Prompt for a password (min 6 chars). If confirm=True ask twice."""
    while True:
        password = input("  Password: ").strip()
        if len(password) < 6:
            print("  Your password is too short. Please use at least 6 characters.")
            continue
        if confirm:
            password2 = input("  Confirm password: ").strip()
            if password != password2:
                print("  The passwords you entered do not match. Please try again.")
                continue
        return password


# -- Public: profile path for a given user ------------------------------------

def profile_path(username):
    """Return the path to this user's profile JSON file."""
    _ensure_dirs()
    return os.path.join(PROFILES_DIR, f"{username}.json")


# -- Public: register ---------------------------------------------------------

def register():
    """
    Walk the user through creating an account.
    Returns the new username on success, or None if they cancel.
    """
    print("\n" + "=" * 45)
    print("            CREATE AN ACCOUNT")
    print("=" * 45)
    print("  Type 'back' at any prompt to return to the main menu.\n")

    users = _load_users()

    while True:
        username = _get_username()
        if username == "back":
            return None
        if username in users:
            print(f"  Sorry, the username '{username}' is already taken. Please choose a different one.")
        else:
            break

    password = _get_password(confirm=True)
    if password.lower() == "back":
        return None

    salt, hashed = _hash_password(password)
    users[username] = {"salt": salt, "password": hashed}
    _save_users(users)

    print(f"\n  Your account has been created successfully! You can now log in as '{username}'.")
    return username


# -- Public: login ------------------------------------------------------------

def login():
    """
    Ask for username + password.
    Returns the username on success, or None after 3 failed attempts.
    """
    print("\n" + "=" * 45)
    print("                  LOG IN")
    print("=" * 45)

    users = _load_users()
    MAX_ATTEMPTS = 3

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n  Attempt {attempt} of {MAX_ATTEMPTS}")
        username = input("  Username: ").strip().lower()
        password = input("  Password: ").strip()

        if username not in users:
            print("  We could not find an account with that username. Please check and try again.")
            continue

        stored    = users[username]
        salt      = stored["salt"]
        _, hashed = _hash_password(password, salt)

        if hashed == stored["password"]:
            print(f"\n  Good to have you back, {username}! Your session is now active.")
            return username
        else:
            remaining = MAX_ATTEMPTS - attempt
            if remaining > 0:
                print(f"  That password is incorrect. You have {remaining} attempt(s) remaining.")
            else:
                print("  You have used all your login attempts. Please return to the main menu and try again.")

    return None


# -- Public: auth gate --------------------------------------------------------

def auth_gate():
    """
    Show the opening menu and return a logged-in username,
    or None if the user chooses to exit.
    """
    while True:
        print("\n" + "=" * 45)
        print("       WELCOME TO KULTURE KONNECT")
        print("=" * 45)
        print("  1. Log In")
        print("  2. Register")
        print("  3. Exit")

        choice = input("\n  Choose an option (1-3): ").strip()

        if choice == "1":
            username = login()
            if username:
                return username

        elif choice == "2":
            username = register()
            if username:
                print("\n  Great! Please log in with your new account to continue.")
                username = login()
                if username:
                    return username

        elif choice == "3":
            print("\n  Thank you for using KultureKonnect. See you next time!")
            return None

        else:
            print("  That is not a valid option. Please enter 1, 2, or 3.")

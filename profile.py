#!/usr/bin/env python3
"""
profile.py - Per-user profile creation and loading.

Profiles are stored in profiles/<username>.json so each user
has their own separate data.
"""

import json
import os


# -- Reusable helpers ----------------------------------------------------------

def pick_from_menu(prompt, options):
    """Display a numbered list; loop until a valid number is entered."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")
    while True:
        choice = input("  Enter the number of your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"  That is not a valid choice. Please enter a number between 1 and {len(options)}.")


def get_text_input(prompt, letters_only=False):
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = input(f"  {prompt}").strip()
        if not value:
            print("  This field cannot be empty. Please enter a value.")
            continue
        if letters_only and not all(c.isalpha() or c.isspace() for c in value):
            print("  Please use letters only. Numbers and symbols are not accepted here.")
            continue
        return value


def get_age_input():
    """Keep asking until a whole number between 5 and 120 is entered."""
    while True:
        value = input("  What is your age? ").strip()
        if value.isdigit():
            age = int(value)
            if 5 <= age <= 120:
                return age
            print("  Please enter a realistic age between 5 and 120.")
        else:
            print("  Age must be a whole number, for example 21. Please try again.")


# -- Profile creation ----------------------------------------------------------

def create_profile(profile_file):
    """
    Collect profile details from the user and save to profile_file.
    Returns the profile dict.
    """
    print("\n" + "=" * 45)
    print("          COMPLETE YOUR PROFILE")
    print("=" * 45)
    print("  Let us get to know you a little better.\n")

    name   = get_text_input("What is your full name? ", letters_only=True)
    age    = get_age_input()
    gender = pick_from_menu(
        "What is your gender?",
        ["Male", "Female", "Non-binary", "Prefer not to say"],
    )
    budget = pick_from_menu(
        "What is your typical budget for activities?",
        ["Low", "Medium", "High"],
    )
    city   = get_text_input("What city or country are you based in? ")

    user_profile = {
        "name":   name,
        "age":    age,
        "gender": gender,
        "budget": budget,
        "city":   city,
    }

    os.makedirs(os.path.dirname(profile_file), exist_ok=True)

    try:
        with open(profile_file, "w") as f:
            json.dump(user_profile, f, indent=2)
        print(f"\n  Your profile has been saved. Welcome to KultureKonnect, {name}!")
    except OSError as e:
        print(f"\n  WARNING: Could not save your profile to disk: {e}")
        print("  Your session will continue, but your details will not be remembered next time.")

    return user_profile


# -- Profile loading -----------------------------------------------------------

def load_profile(profile_file):
    """
    Load a user's profile from profile_file.
    Returns the profile dict, or None if missing / corrupted / incomplete.
    """
    if not os.path.exists(profile_file):
        return None
    try:
        with open(profile_file, "r") as f:
            user_profile = json.load(f)
        required = {"name", "age", "gender", "budget", "city"}
        if not required.issubset(user_profile.keys()):
            print("  Your saved profile is missing some information. Let us fill it in again.")
            return None
        return user_profile
    except (json.JSONDecodeError, OSError):
        print("  We could not read your saved profile. Let us start fresh.")
        return None


# -- Public entry point --------------------------------------------------------

def get_or_create_profile(username, profile_file):
    """
    Load the profile for `username` if it exists, otherwise create it.
    """
    user_profile = load_profile(profile_file)

    if user_profile:
        print(f"\n  Profile loaded. Hello again, {user_profile['name']}!")
    else:
        print(f"\n  Hello {username}, it looks like you have not set up your profile yet.")
        user_profile = create_profile(profile_file)

    return user_profile

# -- Saving profile --------------------------------------------------------

def save_profile(profile_file, user_profile):
    # Write user_profile dictionary back to the profile_file JSON 
    try:
        with open(profile_file, "w") as f:
            json.dump(user_profile, f, indent=2)
    except OSError as e:
        print(f"  WARNING: Could not save profile: {e}")

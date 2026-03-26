#!/usr/bin/env python3
import ui

# -- Reusable helper -----------------------------------------------------------
def pick_from_menu(prompt, options):
    """
    Display a numbered list and loop until the user picks a valid number.
    Returns the chosen string.
    """
    return ui.pick_menu(prompt, options)

# -- Main Menu -----------------------------------------------------------------
def load_main_menu():
    ui.main_menu()
    
    while True:
        choice = input(ui.Fore.YELLOW + "  ▶  Enter your choice (1-3): " + ui.RESET).strip()
        if choice in ("1", "2", "3"):
            return choice
        ui.error("  Invalid choice. Please enter 1, 2 or 3")

# -- Preferences ---------------------------------------------------------------
def get_preferences():
    ui.preferences_header()
    preferences = {}
    preferences["activity"] = pick_from_menu(
        "What kind of activity are you in the mood for?",
        ["Movies", "Games", "Music", "Food & Drinks"],
    )
    preferences["noise_level"] = pick_from_menu(
        "What noise level do you prefer?",
        ["Low", "Medium", "High"],
    )
    preferences["time"] = pick_from_menu(
        "What time of day works best for you?",
        ["Morning", "Afternoon", "Evening"],
    )
    ui.info("Perfect. Your preferences have been noted.")
    return preferences

# -- Entry point ---------------------------------------------------------------
if __name__ == "__main__":
    user_preferences = {}
    while True:
        choice = load_main_menu()
        if choice == "1":
            user_preferences = get_preferences()
            ui.subheader("\n  Your selected preferences:")
            for key, value in user_preferences.items():
                print(f"    {key.replace('_', ' ').capitalize()}: {value}")
        elif choice == "2":
            ui.info("\n  [Rate past attended events - coming soon]")
        elif choice == "3":
            ui.goodbye()
            break

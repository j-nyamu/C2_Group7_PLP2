# -- Reusable helper -----------------------------------------------------------
def pick_from_menu(prompt, options):
    """
    Display a numbered list and loop until the user picks a valid number.
    Returns the chosen string.
    """
    print(f"\n{prompt}")
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")
    while True:
        choice = input("  Enter the number of your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"  That is not a valid choice. Please enter a number between 1 and {len(options)}.")


# -- Main Menu -----------------------------------------------------------------
def load_main_menu():
    print("\n" + "=" * 45)
    print("          MAIN MENU")
    print("=" * 45)
    print("  What would you like to do today.\n")
    print("  1. Set your preferences")
    print("  2. Rate past attended events")
    print("  3. Exit")
    while True:
        choice = input("\n Enter your choice (1-3): ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print(" Invalid choice. Please enter 1, 2 or 3")


# -- Preferences ---------------------------------------------------------------
def get_preferences():
    print("\n" + "=" * 45)
    print("          SET YOUR PREFERENCES")
    print("=" * 45)
    print("  Tell us what kind of experience you are looking for today.\n")
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
    print("\n  Perfect. Your preferences have been noted.")
    return preferences


# -- Entry point ---------------------------------------------------------------
if __name__ == "__main__":
    user_preferences = {}

    while True:
        choice = load_main_menu()

        if choice == "1":
            user_preferences = get_preferences()
            print("\n  Your selected preferences:")
            for key, value in user_preferences.items():
                print(f"    {key.replace('_', ' ').capitalize()}: {value}")

        elif choice == "2":
            print("\n  [Rate past attended events - coming soon]")

        elif choice == "3":
            print("\n  Goodbye! See you next time.\n")
            break
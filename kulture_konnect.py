#!bin/usr/python3

import recommender
import preference_menu


def main():
    print("Welcome to Kulture Konnect!")
    print("Let's start by creating your profile.")
    # Devis to add block
    # profile = create_profile()

    print("\nNow, let's set your preferences.")
    preferences = preference_menu.get_preferences()

    print("\nFinding events that match your preferences...")
    events = recommender.load_events()
    matches = recommender.get_recommendations(profile, preferences, events)

    if matches:
        print("\nHere are some events you might be interested in:")
        for match in matches:
            print(f"{match['name']} - {match['type']} ({match['budget']} budget)")
    else:
        print(
            "\nNo events matched your preferences. Please broaden your search preferences."
        )


# NG: This will on ly run if this file is executed directly, not when imported as a module in another file.

if __name__ == "__main__":
    main()

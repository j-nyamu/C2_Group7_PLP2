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

    # -- Step 4: Load events --------------------------------------------------
    print("\n  Searching for events that match your preferences...")
    events = recommender.load_events()

    if not events:
        print("  There are no events available at the moment. Please check back later.")
        return

    # -- Step 5: Filter and display results ------------------------------------
    matches = recommender.get_recommendations(user_profile, preferences, events)

    print("\n\033[32m" + "=" * 45)
    if matches:
        print(
            f"  We found {len(matches)} event(s) just for you, {user_profile['name']}!\n"
        )
        for i, match in enumerate(matches, start=1):
            print(f"  {i}. {match['name']}")
            print(f"     Location : {match['city']}")
            print(f"     Type     : {match['type']}")
            print(f"     Budget   : {match['budget']}")
            print(f"     Time     : {match['time']}")
            if match.get("description"):
                print(f"     Details  : {match['description']}")
            print()
    else:
        print(
            "\nNo events matched your preferences. Please broaden your search preferences."
        )


# NG: This will on ly run if this file is executed directly, not when imported as a module in another file.

if __name__ == "__main__":
    main()

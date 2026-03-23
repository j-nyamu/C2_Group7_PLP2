#!bin/usr/python3

import time

import recommender
import preference_menu
import rec_ratings


def main():
    print("Welcome to Kulture Konnect!")
    print("Let's start by creating your profile.")
    # Devis to add block

    def create_profile():
        name = input("Enter your name: ")
        while True:
            age_input = input("Enter your age: ")
            if age_input.isdigit() and int(age_input) > 0:
                age = int(age_input)
                break
            else:
                print("Invalid input. Please enter a valid age.")
        city = input("Enter your city: ")
        budget_levels = ["Low", "Medium", "High"]
        print("Select your budget level:")
        for i, level in enumerate(budget_levels, start=1):
            print(f"{i}. {level}")
        while True:
            budget_choice = input("Enter the number of your choice: ")
            if budget_choice.isdigit() and 1 <= int(budget_choice) <= len(
                budget_levels
            ):
                budget = budget_levels[int(budget_choice) - 1]
                break
            else:
                print("Invalid input. Please enter a number from the list.")
        return {"name": name, "age": age, "city": city, "budget": budget}

    # profile = create_profile()

    # print("\nProfile created successfully!")

    # print("\nNow, let's set your preferences.")
    # preferences = preference_menu.get_preferences()

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
    time.sleep(2)

    print("\n Would you like to rate any of the events you attended? (yes/no)")
    while True:
        choice = input("Enter your choice: ").strip().lower()
        if choice in ["yes", "y"]:
            import rec_ratings

            rec_ratings.save_events_rating()
            break
        elif choice in ["no", "n"]:
            print("Thank you for using Kulture Konnect! Goodbye!")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


# NG: This will on ly run if this file is executed directly, not when imported as a module in another file.

if __name__ == "__main__":
    main()

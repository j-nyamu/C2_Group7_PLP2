#!bin/usr/python3
# Code block for recommendations rating

import recommender
import preference_menu
import json


# Function to append user ratings to the events in venue_database.json
def save_events_rating(current_user):
    with open("venue_database.json", "r") as file:
        events = json.load(file)

    event_name = input("Enter event name: ")
    rating = input("Enter rating (1-5): ")

    if not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        print("Invalid rating. Please enter a number between 1 and 5.")
        return

    rating = int(rating)
    found = False

    for event in events:
        if event["name"].strip().lower() == event_name.strip().lower():
            if "ratings" not in event or not isinstance(event["ratings"], dict):
                event["ratings"] = {}

            # one rating per user: overwrite if they already rated
            event["ratings"][current_user] = rating

            with open("venue_database.json", "w") as file:
                json.dump(events, file, indent=4)

            print(f"Rating saved for {event['name']} by {current_user}.")
            found = True
            break

    if not found:
        print("Event not found. Please check the name and try again.")

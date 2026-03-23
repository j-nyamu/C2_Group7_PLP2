#!bin/usr/python3
import json


# Read .json file
def load_events():
    with open("venue_database.json", "r") as file:
        events = json.load(file)
    return events


# Check budget function
def budget_fits(event_budget, user_budget):
    levels = {"Low": 1, "Medium": 2, "High": 3}
    return levels[event_budget] <= levels[user_budget]


# Recommendation Filter Function
def get_recommendations(profile, preferences, events):
    results = []
    for event in events:
        if event["city"].lower() != profile["city"].lower():
            continue
        if not budget_fits(event["budget"], profile["budget"]):
            continue
        if event["type"] not in preferences["activity"]:  # Confirm with Karyna's code
            continue
        if event["min_age"] > profile["age"]:
            continue
        if (
            "preferred_times" in preferences
            and event["time"] not in preferences["preferred_times"]
        ):
            continue

    def avg_rating(event):
        ratings = event.get("ratings", {})
        if isinstance(ratings, dict) and ratings:
            vals = list(ratings.values())
            return sum(vals) / len(vals)
        return 0
        results.sort(
            key=avg_rating, reverse=True
        )  # Sort by average rating, highest first
        results.append(event)

    if len(results) == 0:
        print(
            "No events matched your preferences. Please broaden your search preferences"
        )
    return results


# # Fake profile (Person 1 will build the real version)
# test_profile = {"name": "Alice", "age": 20, "city": "Kigali", "budget": "Medium"}

# # Fake preferences (Person 2 will build the real version)
# test_preferences = {"activity_types": ["Music", "Games"]}

# events = load_events()
# matches = get_recommendations(test_profile, test_preferences, events)

# for match in matches:
#     print(f"{match['name']} - {match['type']} ({match['budget']} budget)")

#!/usr/bin/env python3
import json
import os

EVENTS_FILE = "venue_database.json"


# -- Load events safely --------------------------------------------------------
def load_events():
    """Load the venue database. Returns empty list if file is missing or broken."""
    if not os.path.exists(EVENTS_FILE):
        print(f"  WARNING: The events file '{EVENTS_FILE}' could not be found. Please make sure it is in the project folder.")
        return []
    try:
        with open(EVENTS_FILE, "r") as file:
            events = json.load(file)
        if not isinstance(events, list):
            print("  WARNING: The events file does not contain a valid list of events.")
            return []
        return events
    except json.JSONDecodeError:
        print("  WARNING: The events file appears to be corrupted and could not be read.")
        return []


# -- Budget comparison ---------------------------------------------------------
def budget_fits(event_budget, user_budget):
    """Return True if the event budget is within the user's budget."""
    levels = {"Low": 1, "Medium": 2, "High": 3}
    event_level = levels.get(event_budget, 0)
    user_level  = levels.get(user_budget, 0)
    return event_level <= user_level


# -- Recommendation filter -----------------------------------------------------
def get_recommendations(profile, preferences, events):
    """
    Filter events against the user's profile and preferences.
    All comparisons are case-insensitive and type-safe.
    """
    results = []
    required_event_keys = {"city", "budget", "type", "min_age", "time", "name"}

    for event in events:
        if not required_event_keys.issubset(event.keys()):
            continue
        if event["city"].strip().lower() != str(profile.get("city", "")).strip().lower():
            continue
        if not budget_fits(event["budget"], profile.get("budget", "Low")):
            continue
        if event["type"].strip().lower() != preferences.get("activity", "").strip().lower():
            continue
        if event["min_age"] > int(profile.get("age", 0)):
            continue
        if event["time"].strip().lower() != preferences.get("time", "").strip().lower():
            continue
        results.append(event)

    return results

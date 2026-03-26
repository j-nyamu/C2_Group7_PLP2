#!/usr/bin/env python3
from db import get_connection


# -- Budget comparison ---------------------------------------------------------
def budget_fits(event_budget, user_budget):
    """Return True if the event budget is within the user's budget."""
    levels = {"Low": 1, "Medium": 2, "High": 3}
    event_level = levels.get(event_budget, 0)
    user_level  = levels.get(user_budget, 0)
    return event_level <= user_level


# -- Load events from MySQL ----------------------------------------------------
def load_events():
    """
    Load all venues from the database with their average rating.
    Returns a list of dicts using the same keys the rest of the app expects.
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT v.name,
                   v.type,
                   v.city,
                   v.budget,
                   v.noise,
                   v.min_age,
                   v.time_of_day  AS time,
                   v.description,
                   COALESCE(AVG(r.rating), 0) AS avg_rating
            FROM   venues v
            LEFT JOIN venue_ratings r ON r.venue_id = v.id
            GROUP  BY v.id
            """
        )
        events = cursor.fetchall()
        cursor.close()
        conn.close()
        return events
    except Exception as e:
        print(f"  WARNING: Could not load events from database: {e}")
        return []


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

    results.sort(key=lambda e: e.get("avg_rating", 0), reverse=True)
    return results

#!/usr/bin/env python3
from db import get_connection


def save_events_rating(current_user_id):

    # Prompt the user for an event name and rating, then save to the database.
    # current_user_id: the integer id of the logged-in user (from users table).
    # One rating per user per venue; re-rating overwrites the previous value.

    event_name = input("Enter event name: ").strip()
    rating = input("Enter rating (1-10): ").strip()

    if not rating.isdigit() or not (1 <= int(rating) <= 10):
        print("Invalid rating. Please enter a number between 1 and 10.")
        return

    rating = int(rating)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Look up venue by name (case-insensitive)
        cursor.execute(
            "SELECT id, name FROM venues WHERE LOWER(name) = LOWER(%s)",
            (event_name,),
        )
        row = cursor.fetchone()
        if not row:
            print("Event not found. Please check the name and try again.")
            cursor.close()
            conn.close()
            return

        venue_id, venue_name = row

        # Upsert: insert or overwrite existing rating
        cursor.execute(
            """INSERT INTO venue_ratings (venue_id, user_id, rating)
               VALUES (%s, %s, %s)
               ON DUPLICATE KEY UPDATE rating = VALUES(rating)""",
            (venue_id, current_user_id, rating),
        )
        conn.commit()
        print(f"Rating saved for {venue_name}.")

    except Exception as e:
        print(f"  ERROR: Could not save rating: {e}")
    finally:
        cursor.close()
        conn.close()

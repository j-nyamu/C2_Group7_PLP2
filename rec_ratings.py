#!/usr/bin/env python3
from db import get_connection


def save_events_rating(current_user_id):
    """
    Show venues attended by this user and allow rating one of them.
    One rating per user per venue; re-rating overwrites the previous value.
    """
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Pull only venues this user has actually attended via saved actions.
        cursor.execute(
            """
            SELECT v.id,
                   v.name,
                   MAX(ua.timestamp) AS last_attended,
                   COUNT(*)          AS times_attended
            FROM user_actions ua
            JOIN venues v ON LOWER(v.name) = LOWER(ua.event_name)
            WHERE ua.user_id = %s
            GROUP BY v.id, v.name
            ORDER BY last_attended DESC, v.name ASC
            """,
            (current_user_id,),
        )
        attended = cursor.fetchall()

        if not attended:
            print("You do not have any attended events yet.")
            print(
                "Try selecting an event and choosing itinerary/reservation/ticket first."
            )
            return

        print("\nRate a past attended event:\n")
        for i, row in enumerate(attended, start=1):
            print(f"  {i}. {row['name']}")
        print(f"  {len(attended) + 1}. Return to Main Menu")

        selected = None
        while True:
            choice = input("\n  Enter event number: ").strip()
            if not choice.isdigit():
                print("  Please enter a valid number.")
                continue
            idx = int(choice)
            if idx == len(attended) + 1:
                print("  Returning to Main Menu...")
                return
            if 1 <= idx <= len(attended):
                selected = attended[idx - 1]
                break
            print(f"  Please enter a number between 1 and {len(attended) + 1}.")

        while True:
            rating_raw = input("Enter rating (1-10): ").strip()
            if rating_raw.isdigit() and 1 <= int(rating_raw) <= 10:
                rating = int(rating_raw)
                break
            print("Invalid rating. Please enter a number between 1 and 10.")

        cursor.execute(
            """INSERT INTO venue_ratings (venue_id, user_id, rating)
               VALUES (%s, %s, %s)
               ON DUPLICATE KEY UPDATE rating = VALUES(rating)""",
            (selected["id"], current_user_id, rating),
        )
        conn.commit()
        print(f"Rating saved for {selected['name']}.")

    except Exception as e:
        print(f"  ERROR: Could not save rating: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#!/usr/bin/env python3
"""
migrate.py - One-time script to seed the PLP2 MySQL database from existing JSON files.

Run ONCE after creating the tables with setup.sql:
    python migrate.py

Safe to re-run (INSERT IGNORE skips already-migrated rows).
"""

import json
import os
import glob
from db import get_connection


def migrate():
    conn = get_connection()
    cursor = conn.cursor()

    profiles_migrated = 0
    actions_migrated  = 0
    venues_migrated   = 0
    ratings_migrated  = 0

    # ------------------------------------------------------------------
    # 1. Migrate profiles/*.json -> profiles + user_actions tables
    # ------------------------------------------------------------------
    print("Migrating profiles and actions...")
    for profile_path in glob.glob(os.path.join("profiles", "*.json")):
        username = os.path.splitext(os.path.basename(profile_path))[0]

        # Resolve user_id
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        if not row:
            print(f"  WARNING: No user '{username}' in users table — skipping {profile_path}")
            continue
        user_id = row[0]

        with open(profile_path, "r") as f:
            pdata = json.load(f)

        cursor.execute(
            """INSERT IGNORE INTO profiles (user_id, name, age, gender, budget, city)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                user_id,
                pdata.get("name", ""),
                pdata.get("age", 0),
                pdata.get("gender", ""),
                pdata.get("budget", "Low"),
                pdata.get("city", ""),
            ),
        )
        if cursor.rowcount:
            profiles_migrated += 1

        # Migrate action history
        actions = pdata.get("actions", {})
        for action_type, entries in actions.items():
            if action_type not in ("Itinerary", "Reservation", "Ticket"):
                continue
            for entry in entries:
                cursor.execute(
                    """INSERT IGNORE INTO user_actions (user_id, action_type, event_name, timestamp)
                       VALUES (%s, %s, %s, %s)""",
                    (user_id, action_type, entry.get("event", ""), entry.get("timestamp")),
                )
                if cursor.rowcount:
                    actions_migrated += 1

        conn.commit()

    # ------------------------------------------------------------------
    # 3. Migrate venue_database.json -> venues + venue_ratings tables
    # ------------------------------------------------------------------
    print("Migrating venues and ratings...")
    if os.path.exists("venue_database.json"):
        with open("venue_database.json", "r") as f:
            venues_data = json.load(f)

        for venue in venues_data:
            cursor.execute(
                """INSERT IGNORE INTO venues
                       (name, type, city, budget, noise, min_age, time_of_day, description)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    venue.get("name", ""),
                    venue.get("type", ""),
                    venue.get("city", ""),
                    venue.get("budget", "Low"),
                    venue.get("noise", "Low"),
                    venue.get("min_age", 0),
                    venue.get("time", ""),        # JSON key is "time", column is "time_of_day"
                    venue.get("description", ""),
                ),
            )
            if cursor.rowcount:
                venues_migrated += 1

            # Get venue_id for ratings
            cursor.execute("SELECT id FROM venues WHERE name = %s", (venue.get("name"),))
            venue_row = cursor.fetchone()
            if not venue_row:
                continue
            venue_id = venue_row[0]

            ratings = venue.get("ratings", {})
            if not isinstance(ratings, dict):
                continue

            for username, rating_val in ratings.items():
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                user_row = cursor.fetchone()
                if not user_row:
                    continue
                cursor.execute(
                    """INSERT IGNORE INTO venue_ratings (venue_id, user_id, rating)
                       VALUES (%s, %s, %s)""",
                    (venue_id, user_row[0], int(rating_val)),
                )
                if cursor.rowcount:
                    ratings_migrated += 1

        conn.commit()
    else:
        print("  venue_database.json not found — skipping.")

    cursor.close()
    conn.close()

    print("\nMigration complete!")
    print(f"  Profiles : {profiles_migrated}")
    print(f"  Actions  : {actions_migrated}")
    print(f"  Venues   : {venues_migrated}")
    print(f"  Ratings  : {ratings_migrated}")


if __name__ == "__main__":
    migrate()

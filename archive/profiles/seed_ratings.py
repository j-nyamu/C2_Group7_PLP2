#!/usr/bin/env python3
"""
seed_ratings.py - Widen the venue_ratings CHECK constraint to 1-10,
then insert random ratings for 9 randomly chosen venues.

Run once:
    python seed_ratings.py
"""

import random
from db import get_connection


def widen_constraint(cursor):
    """Drop the old CHECK (1-5) constraint and add CHECK (1-10)."""
    # Find the current check constraint name for venue_ratings.rating
    cursor.execute(
        """
        SELECT CONSTRAINT_NAME
        FROM   information_schema.TABLE_CONSTRAINTS
        WHERE  TABLE_SCHEMA   = DATABASE()
          AND  TABLE_NAME     = 'venue_ratings'
          AND  CONSTRAINT_TYPE = 'CHECK'
        """
    )
    rows = cursor.fetchall()
    for (name,) in rows:
        try:
            cursor.execute(f"ALTER TABLE venue_ratings DROP CHECK `{name}`")
            print(f"  Dropped constraint: {name}")
        except Exception as e:
            print(f"  Could not drop {name}: {e}")

    cursor.execute(
        "ALTER TABLE venue_ratings ADD CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 10)"
    )
    print("  Added constraint: chk_rating (1-10)")


def seed():
    conn   = get_connection()
    cursor = conn.cursor()

    # Widen the CHECK constraint
    print("Updating CHECK constraint...")
    widen_constraint(cursor)
    conn.commit()

    # Fetch all venue IDs
    cursor.execute("SELECT id, name FROM venues ORDER BY id")
    venues = cursor.fetchall()
    if len(venues) < 9:
        print(f"Only {len(venues)} venues found; seeding all of them.")
        chosen = venues
    else:
        chosen = random.sample(venues, 9)

    # Fetch all user IDs
    cursor.execute("SELECT id FROM users")
    user_ids = [r[0] for r in cursor.fetchall()]
    if not user_ids:
        print("No users found in the database — cannot insert ratings (need a user_id).")
        cursor.close()
        conn.close()
        return

    print(f"\nSeeding ratings for {len(chosen)} venues...")
    inserted = 0
    for venue_id, venue_name in chosen:
        user_id = random.choice(user_ids)
        rating  = random.randint(1, 10)
        cursor.execute(
            """INSERT INTO venue_ratings (venue_id, user_id, rating)
               VALUES (%s, %s, %s)
               ON DUPLICATE KEY UPDATE rating = VALUES(rating)""",
            (venue_id, user_id, rating),
        )
        inserted += cursor.rowcount
        print(f"  {venue_name:<40} -> {rating}/10  (user_id={user_id})")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"\nDone. {inserted} rating(s) inserted/updated.")


if __name__ == "__main__":
    seed()

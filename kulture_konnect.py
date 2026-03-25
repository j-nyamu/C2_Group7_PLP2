#!/usr/bin/env python3
import auth
import recommender
import preference_menu
import profile
import post_actions
import rec_ratings


def main():
    # -- Step 1: Authenticate --------------------------------------------------
    username = auth.auth_gate()
    if username is None:
        return

    # -- Step 2: Resolve user_id and load / create profile --------------------
    user_id = auth.get_user_id(username)
    user_profile = profile.get_or_create_profile(username, user_id)

    # -- Step 3: Load Main Menu --------------------------------------------------
    while True:
        menu_choice = preference_menu.load_main_menu()
        if menu_choice == "1":
            # -- Step 4: Preferences --------------------------------------------------
            print(
                f"\n  Wonderful, {user_profile['name']}! Let us find something great for you."
            )
            preferences = preference_menu.get_preferences()
        if menu_choice == "2":
            rec_ratings.save_events_rating(user_id)
            continue
        if menu_choice == "3":
            print("\n  Thank you for using KultureKonnect. See you next time!")
        break

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
            avg = float(match.get("avg_rating") or 0)
            rating_text = (
                "Not Yet Rated" if avg <= 0 else f"{avg:.if}/10"
            )  # Prints text instead of just 0/10 for rating
            print(f"     Rating   : {rating_text}")
            if match.get("description"):
                print(f"     Details  : {match['description']}")
            print()
    else:
        print(
            f"  We could not find any events that match your current preferences, {user_profile['name']}."
        )
        print(
            "  Consider choosing a higher budget or a different time of day and try again."
        )
    print("=" * 45)
    print("\033[0m")

    # -- Step 6: Post Recommendation Actions ------------------------------------
    post_actions.show_post_actions_menu(matches, user_id)


if __name__ == "__main__":
    main()

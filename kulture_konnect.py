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

    # -- Step 3+: Main app loop -------------------------------------------------
    while True:
        menu_choice = preference_menu.load_main_menu()

        if menu_choice == "1":
            print(
                f"\n  Wonderful, {user_profile['name']}! Let us find something great for you."
            )
            preferences = preference_menu.get_preferences()

            print("\n  Searching for events that match your preferences...")
            events = recommender.load_events()

            if not events:
                print(
                    "  There are no events available at the moment. Please check back later."
                )
                continue

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
                    rating_text = "Not Yet Rated" if avg <= 0 else f"{avg:.1f}/10"
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

            action_result = post_actions.show_post_actions_menu(matches, user_id)
            if action_result == "main_menu":
                continue

            continue

        elif menu_choice == "2":
            rec_ratings.save_events_rating(user_id)
            continue

        elif menu_choice == "3":
            print("\n  Thank you for using KultureKonnect. See you next time!")
            break


if __name__ == "__main__":
    main()

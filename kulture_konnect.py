#!/usr/bin/env python3
import auth
import recommender
import preference_menu
import profile
import post_actions


def main():
    # -- Step 1: Authenticate --------------------------------------------------
    username = auth.auth_gate()
    if username is None:
        return

    # -- Step 2: Load / create this user's profile ----------------------------
    pfile        = auth.profile_path(username)
    user_profile = profile.get_or_create_profile(username, pfile)

    # -- Step 3: Preferences --------------------------------------------------
    print(f"\n  Wonderful, {user_profile['name']}! Let us find something great for you.")
    preferences = preference_menu.get_preferences()

    # -- Step 4: Load events --------------------------------------------------
    print("\n  Searching for events that match your preferences...")
    events = recommender.load_events()

    if not events:
        print("  There are no events available at the moment. Please check back later.")
        return

    # -- Step 5: Filter and display results ------------------------------------
    matches = recommender.get_recommendations(user_profile, preferences, events)

    print("\n" + "=" * 45)
    if matches:
        print(f"  We found {len(matches)} event(s) just for you, {user_profile['name']}!\n")
        for i, match in enumerate(matches, start=1):
            print(f"  {i}. {match['name']}")
            print(f"     Location : {match['city']}")
            print(f"     Type     : {match['type']}")
            print(f"     Budget   : {match['budget']}")
            print(f"     Time     : {match['time']}")
            if match.get("description"):
                print(f"     Details  : {match['description']}")
            print()
    else:
        print(f"  We could not find any events that match your current preferences, {user_profile['name']}.")
        print("  Consider choosing a higher budget or a different time of day and try again.")
    print("=" * 45)

    # -- Step 6: Post Recommendation Actions ------------------------------------
    post_actions.show_post_actions_menu(matches)



if __name__ == "__main__":
    main()

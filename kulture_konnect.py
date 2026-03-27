#!/usr/bin/env python3
import auth
import recommender
import preference_menu
import profile
import post_actions
import rec_ratings

import ui 


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
            ui.info(
                f"\n  Wonderful, {user_profile['name']}! Let us find something great for you."
            )
            preferences = preference_menu.get_preferences()

            ui.info("\n  Searching for events that match your preferences...")
            events = recommender.load_events()

            if not events:
                ui.warn(
                    "  There are no events available at the moment. Please check back later."
                )
                continue

            matches = recommender.get_recommendations(user_profile, preferences, events)

            ui.info("\n  Here are some events that might interest you:")
            if matches:
                ui.recommendations_header(user_profile["name"], len(matches))
                
                for i, match in enumerate(matches, start=1):
                  ui.recommendation_card(i, match)
            else:
                ui.no_recommendations(user_profile["name"])

            action_result = post_actions.show_post_actions_menu(matches, user_id)
            if action_result == "main_menu":
                continue

            continue

        elif menu_choice == "2":
            rec_ratings.save_events_rating(user_id)
            continue

        elif menu_choice == "3":
            ui.goodbye()
            break


if __name__ == "__main__":
    main()

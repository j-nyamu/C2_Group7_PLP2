from datetime import datetime
import json
import profile # To use the save_profile function


def show_post_actions_menu(matches, profile_file):
    #Let user select an event from the list then show action menu afterwards

    if not matches:
        print("No matches available")
        return
    
    #PART 1 - SELECT AN EVENT

    print("\nChoose your preferred activity\n\n")
    for i, event in enumerate(matches, start=1):
        print(f" {i}. {event['name']} ({event['type']})")
    
    while True:
        try:
            choice = int(input("\n  Enter the event number: "))
            if 1 <= choice <= len(matches):
                selected_event = matches[choice - 1]
                break
            else:
                print(f"  Please enter a number between 1 and {len(matches)}.")
        except ValueError:
            print("  Please enter a valid number.")

    print(f"\n\033[32m  --- Selected: {selected_event['name']} ---\033[0m\n")

    #PART 2 - SHOW ACTION MENU
    print("  1. Schedule an Itinerary")
    print("  2. Make a Reservation")
    print("  3. Buy Tickets")
    print("  4. Return to Main Menu")
    while True:
        action = input("\n  Enter your action choice (1-4): ").strip()
        if action == "1":
            handle_itinerary(selected_event, profile_file)
            break
        elif action == "2":
            handle_reservation(selected_event, profile_file)
            break
        elif action == "3":
            handle_tickets(selected_event, profile_file)
            break
        elif action == "4":
            print("  Returning to Main Menu...")
            break
        else:
            print("  Invalid choice.")

#PART 3 - SAVE THE ACTION TO PROFILE
def add_event_to_history_grouped(profile_file, event_name, action_type):

    try:
        with open(profile_file, "r") as f:
            user_data = json.load(f)
        # 1. Ensure the 'actions' object exists
        if "actions" not in user_data:
            user_data["actions"] = {}
        # 2. Ensure the specific action category exists (like 'Reservations')
        if action_type not in user_data["actions"]:
            user_data["actions"][action_type] = []
        # 3. Create entry and append to the specific category
        new_entry = {
            "event": event_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        user_data["actions"][action_type].append(new_entry)
        # 4. Save
        profile.save_profile(profile_file, user_data)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error updating grouped history: {e}")
    

def handle_itinerary(event, profile_file):
    add_event_to_history_grouped(profile_file, event['name'], "Itinerary")
    print(f"\n\033[32m  [Action] {event['name']} has been added to your itinerary!\n\033[0m")
    print("\033[32m  Thank you for using KultureKonnect! \033[0m \n\n")

def handle_reservation(event, profile_file):
    add_event_to_history_grouped(profile_file, event['name'], "Reservation")
    print(f"\n\033[32m  [Action] Reservation confirmed for {event['name']}.\n\033[0m")
    print("\033[32m  Thank you for using KultureKonnect! \033[0m \n\n")

def handle_tickets(event, profile_file):
    add_event_to_history_grouped(profile_file, event['name'], "Ticket")
    print(f"\n\033[32m  [Action] You've successfully bought tickets for {event['name']}!\n\033[0m")
    print("\033[32m  Thank you for using KultureKonnect! \033[0m \n\n")

        
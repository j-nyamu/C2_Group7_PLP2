def show_post_actions_menu(matches):
    #Let user select an event from the list then show action menu afterwards

    if not matches:
        print("No matches available")
        return
    
    #PART 1 - SELECT AN EVENT

    print("\nChoose your preferred activity")
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

    print(f"\n  --- Selected: {selected_event['name']} ---")

    #PART 2 - SHOW ACTION MENU
    print("  1. Schedule an Itinerary")
    print("  2. Make a Reservation")
    print("  3. Buy Tickets")
    print("  4. Return to Main Menu")
    while True:
        action = input("\n  Enter your action choice (1-4): ").strip()
        if action == "1":
            handle_itinerary(selected_event)
            break
        elif action == "2":
            handle_reservation(selected_event)
            break
        elif action == "3":
            handle_tickets(selected_event)
            break
        elif action == "4":
            print("  Returning to Main Menu...")
            break
        else:
            print("  Invalid choice.")

def handle_itinerary(event):
    print(f"\n  [Action] {event['name']} has been added to your itinerary!")

def handle_reservation(event):
    print(f"\n  [Action] Reservation confirmed for {event['name']}.")

def handle_tickets(event):
    print(f"\n  [Action] You've successfully bought tickets for {event['name']}!")

        
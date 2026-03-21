def get_preferences():
    preferences = {}

    # Activity selection
    types = ["Movies", "Games", "Music", "Food & Drinks",]

    #print the options with numbers
    print("Select your preferred activity: ")
    for i, activity in enumerate(types, start=1):
        print(f"{i}. {activity}") #prints activities with corresponding numbers

    #ask user for their choice
    while True:
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(types):
            choice_index = int(choice) - 1 #because python lists are zero-indexed
            preferences["activity"] = types[choice_index]
            break
        else:
            print("Invalid input. Please enter a number from the list.")

    # Noise level
    noise_levels = ["Low", "Medium", "High"]

    #ask the user for option
    print("Select your preferred noise level: ")
    for i, noise_level in enumerate(noise_levels, start=1):
        print(f"{i}. {noise_level}")  # prints noise_levels with corresponding numbers

    # ask user for their choice
    while True:
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(noise_levels):
            choice_index = int(choice) - 1  # because python lists are zero-indexed
            preferences["noise_level"] = noise_levels[choice_index]
            break
        else:
            print("Invalid input. Please enter a number from the list.")

    # Availability
    times = ["Morning", "Afternoon", "Evening"]

    # ask the user for option
    print("Select your preferred time: ")
    for i, time in enumerate(times, start=1):
        print(f"{i}. {time}")  # prints time with corresponding numbers

    # ask user for their choice
    while True:
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(times):
            choice_index = int(choice) - 1  # because python lists are zero-indexed
            preferences["time"] = times[choice_index]
            break
        else:
            print("Invalid input. Please enter a number from the list.")


    return preferences

if __name__ == "__main__":
    user_preferences = get_preferences()
    print("\nYour selected preferences:")
    for key, value in user_preferences.items():
        print(f"{key.capitalize()}: {value}")

import tools_tracker

# tools_tracker.init_db()

data = tools_tracker.load_menu()

while True:
    print("----- Main Menu -----")
    print("1. Show Movie List")
    print("2. Show Tv Show List")
    print("3. Show Music List")
    print("4. Exit")
    print()

    choice = input("Choose a number to proceed: ")

    if choice == "1":
        # find list
        movie_list = data["Media To Download"]["Movies"]
        
        # check if list has movies
        if len(movie_list) > 0:
            print("----- Movies -----")
            for mov in movie_list:
                print(f"{mov['Name']}: {mov['Year']}: {mov['Downloaded']}")
        else:
            # list is empty
            print("\nYour movie list is empty.")

        user_input = input("Type 'back' to go back or 'exit' to exit: ")

        if user_input.lower() == 'back':
            continue
        elif user_input.lower() == 'exit':
            print("Goodbye!")
            break
    
    elif choice == "2":
        # find list
        tv_show_list = data["Media To Download"]["Tv Shows"]
        
        # check if list has tv shows
        if len(tv_show_list) > 0:
            print("----- Tv Shows -----")
            for show in tv_show_list:
                print(f"\n{show['Name']}: {show['Year']}: {show['Downloaded']}")

                # check if this show has the "Seasons" key
                if "Seasons" in show:
                    # loop through sub-dictionary
                    for s_name, s_status in show["Seasons"].items():
                        status_text = "Done" if s_status else "Needed"
                        print(f"   > {s_name}: {status_text}")

        else:
            # list is empty
            print("\nYour tv show list is empty.")

        user_input = input("Type 'back' to go back or 'exit' to exit: ")

        if user_input.lower() == 'back':
            continue
        elif user_input.lower() == 'exit':
            print("Goodbye!")
            break

    elif choice == "3":
        # find list
        music_list = data["Media To Download"]["Music"]
        
        # check if list has music
        if len(music_list) > 0:
            print("----- Music -----")
            for music in music_list:
                print(f"{music['Name']}: {music['Year']}: {music['Downloaded']}")

                # check for Album key
                if "Album" in music:
                    for a_name, a_status in music["Albums"].items():
                        status_text = "Done" if a_status else "Needed"
                        print(f"   > {a_name}: {status_text}")

        else:
            # list is empty
            print("\nYour music list is empty.")

        user_input = input("Type 'back' to go back or 'exit' to exit: ")

        if user_input.lower() == 'back':
            continue
        elif user_input.lower() == 'exit':
            print("Goodbye!")
            break
    
    elif choice == "4":
        print("\nGoodbye!")
        break
    else:
        print("Invalid choice. Try again.")
import tools_tracker

# tools_tracker.init_db()

data = tools_tracker.load_menu()

try:
    while True:
        print("----- Main Menu -----")
        print("1. Show Movie List")
        print("2. Show Tv Show List")
        print("3. Show Music List")
        print("4. Add Your Item")
        print("5. Exit")
        print()

        choice = input("Choose a number to proceed: ")

        if choice == "1":
            # find list
            movie_list = data["media to download"]["movies"]
            
            # check if list has movies
            if len(movie_list) > 0:
                print("\n----- Movies -----")
                for mov in movie_list:
                    print(f"Name: {mov['name']} | Year: {mov['year']} | Downloaded: {mov['downloaded']}")
            else:
                # list is empty
                print("\nYour movie list is empty.")

            action = tools_tracker.prompt_back_or_exit()
            if action == "exit":
                break
        
        elif choice == "2":
            # find list
            tv_show_list = data["media to download"]["tvshows"]
            
            # check if list has tv shows
            if len(tv_show_list) > 0:
                print("\n----- Tv Shows -----")
                for show in tv_show_list:
                    print(f"Name: {show['name']} | Year: {show['year']}")

                    # check if this show has the "seasons" key
                    if "seasons" in show:
                        # loop through sub-dictionary
                        for s_name, s_status in show["seasons"].items():
                            status_text = "True" if s_status else "Need"
                            print(f"   > {s_name}: {status_text}")

            else:
                # list is empty
                print("\nYour tv show list is empty.")

            action = tools_tracker.prompt_back_or_exit()
            if action == "exit":
                break

        elif choice == "3":
            # find list
            music_list = data["media to download"]["music"]
            
            # check if list has music
            if len(music_list) > 0:
                print("\n----- Music -----")
                for music in music_list:
                    print(f"Artist: {music['name']}")

                    # check for Album key
                    if "album" in music:
                        for a_name, a_info in music["album"].items():
                            status_text = "True" if a_info["downloaded"] else "Need"
                            print(f"   > {a_name} ({a_info['year']}): {status_text}")

            else:
                # list is empty
                print("\nYour music list is empty.")

            action = tools_tracker.prompt_back_or_exit()
            if action == "exit":
                break
        
        elif choice == "4":
            while True:
                print("\n----- Add Item -----")
                raw_cat = input("Category (Movies, Tv Shows, or Music) or type 'goback' to go back to menu: ").strip()
                cat = raw_cat.lower().replace(" ", "")

                if cat == "goback":
                    print("\nReturning to Main Menu...")
                    break
                
                elif cat not in ["movies", "tvshows", "music"]:
                    print("Invalid category. Please type Movies, Tv Shows, or Music.")
                    continue

                name = ""
                year = ""
                is_downloaded = False
                s_data = None
                a_data = None

                if cat == "movies":
                    name = input(f"Enter Movie Name: ")
                    year = input(f"Enter Movie Year: ")
                
                    while True:
                        is_down_raw = input("Is is downloaded? (y/n): ").lower()
                        if is_down_raw in ['y', 'n']:
                            is_downloaded = (is_down_raw == 'y')
                            break
                        print("Invalid input. Please type 'y' or 'n'.")

                elif cat == "tvshows":            
                    name = input("Enter TV Show Name: ")
                    year = input("Enter TV Show Year: ")
                    s_data = {}

                    while True:
                        s_num = input("Enter Season Number (e.g., Season 1) or type 'done' to finish: ").strip()
                        if s_num.lower() == 'done':
                            break
                        
                        # specific season status
                        while True:
                            is_down_raw = input(f"Is {s_num} downloaded? (y/n): ").lower()
                            if is_down_raw in ['y', 'n']:
                                s_data[s_num] = (is_down_raw == 'y')
                                break
                            print("Invalid input. Please type 'y' or 'n'.")

                elif cat == "music":
                    name = input("Enter Band/Artist Name: ")
                    
                    a_data = {}

                    while True:
                        album_name = input("Enter Album Name or type 'done' to finish: ").strip()
                        if album_name.lower() == 'done':
                            break
                        
                        album_year = input(f"Enter Album Year for '{album_name}': ")

                        # ask for this specific album's status
                        while True:
                            is_down_raw = input(f"Is '{album_name}' downloaded? (y/n): ").lower()
                            if is_down_raw in ['y', 'n']:
                                a_data[album_name] = {"year": album_year, "downloaded": (is_down_raw == 'y')}
                                break
                            print("Invalid input. Please type 'y' or 'n'.")

                    if not a_data: a_data = None


                tools_tracker.add_item(data, cat, name, year, downloaded=is_downloaded, seasons=s_data, album=a_data)

                print(f"\n--- {name} has been updated in {cat}! ---")
                
                data = tools_tracker.load_menu()
                break

        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Try again.")

except KeyboardInterrupt:
    print("\n\nForced exit detected. Saving (if needed) and shutting down. Goodbye!")
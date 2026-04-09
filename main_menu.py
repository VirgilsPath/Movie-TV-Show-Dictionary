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
        print("5. Edit Item")
        print("6. Exit")
        print()

        choice = input("Choose a number to proceed: ")

        if choice == "1":
            movie_list = data["media to download"]["movies"]
            if len(movie_list) > 0:
                filter_choice = tools_tracker.prompt_filter()
                
                if filter_choice == "1":
                    filtered = movie_list
                elif filter_choice == "2":
                    filtered = [m for m in movie_list if m['downloaded']]
                elif filter_choice == "3":
                    filtered = [m for m in movie_list if not m['downloaded']]

                print("\n----- Movies -----")
                if len(filtered) > 0:
                    for mov in filtered:
                        print(f"Name: {mov['name']} | Year: {mov['year']} | Downloaded: {mov['downloaded']}")
                else:
                    print("No movies found with that filter.")
            else:
                print("\nYour movie list is empty.")

            action = tools_tracker.prompt_back_or_exit()
            if action == "exit":
                break
        
        elif choice == "2":
            tv_show_list = data["media to download"]["tvshows"]
            if len(tv_show_list) > 0:
                filter_choice = tools_tracker.prompt_filter()

                if filter_choice == "1":
                    filtered = tv_show_list
                elif filter_choice == "2":
                    filtered = [s for s in tv_show_list if "seasons" in s and any(v for v in s["seasons"].values())]
                elif filter_choice == "3":
                    filtered = [s for s in tv_show_list if "seasons" in s and any(not v for v in s["seasons"].values())]

                print("\n----- Tv Shows -----")
                if len(filtered) > 0:
                    for show in filtered:
                        print(f"Name: {show['name']} | Year: {show['year']}")
                        if "seasons" in show:
                            for s_name, s_status in show["seasons"].items():
                                status_text = "Downloaded" if s_status else "Need"
                                print(f"   > {s_name}: {status_text}")
                else:
                    print("No TV shows found with that filter.")
            else:
                print("\nYour TV show list is empty.")

            action = tools_tracker.prompt_back_or_exit()
            if action == "exit":
                break

        elif choice == "3":
            music_list = data["media to download"]["music"]
            if len(music_list) > 0:
                filter_choice = tools_tracker.prompt_filter()

                if filter_choice == "1":
                    filtered = music_list
                elif filter_choice == "2":
                    filtered = [m for m in music_list if "album" in m and any(a["downloaded"] for a in m["album"].values())]
                elif filter_choice == "3":
                    filtered = [m for m in music_list if "album" in m and any(not a["downloaded"] for a in m["album"].values())]

                print("\n----- Music -----")
                if len(filtered) > 0:
                    for music in filtered:
                        print(f"Artist: {music['name']}")
                        if "album" in music:
                            for a_name, a_info in music["album"].items():
                                status_text = "Downloaded" if a_info["downloaded"] else "Need"
                                print(f"   > {a_name} ({a_info['year']}): {status_text}")
                else:
                    print("No music found with that filter.")
            else:
                print("\nYour music list is empty.")

            action = tools_tracker.prompt_back_or_exit()
            if action == "exit":
                break
        
        elif choice == "4":
            print("\n----- Add Item -----")
            raw_cat = input("Category (Movies, Tv Shows, or Music) or type 'goback' to go back to menu: ").strip()
            cat = raw_cat.lower().replace(" ", "")

            if cat == "goback":
                print("\nReturning to Main Menu...")
                break
            elif cat not in ["movies", "tvshows", "music"]:
                print("Invalid category. Please type Movies, Tv Shows, or Music.")
                continue
            else:
                stay_in_add = True
                while stay_in_add:
                    print("\n----- Add Item -----")

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
                            s_raw = input("Enter Season Number or type 'done' to finish: ").strip()
                            if s_raw.lower() == 'done':
                                break
                            
                            if not s_raw.isdigit():
                                print("Invalid input. Please enter a number only (e.g. 1, 2, 3).")
                                continue

                            s_num = f"Season {s_raw}"

                            if s_num in s_data:
                                print(f"{s_num} is already added. Skipping.")
                                continue

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
                    
                    while True:
                        again = input(f"\nAdd another {raw_cat}? (y/n): ").lower()
                        if again == 'y':
                            break # loops back to add another
                        elif again == 'n':
                            stay_in_add = False # exits the add loop > back to main menu
                            print("\nReturning to Main Menu...")
                            break
                        else:
                            print("Invalid input. Please type 'y' or 'n'.")

        elif choice == "5":
            print("\n----- Edit Item -----")
            raw_cat = input("Category (Movies, Tv Shows, or Music) or type 'goback' to go back: ").strip()
            cat = raw_cat.lower().replace(" ", "")

            if cat == "goback":
                print("\nReturning to Main Menu...")
            elif cat == "movies":
                tools_tracker.edit_movie(data)
                data = tools_tracker.load_menu()
            elif cat == "tvshows":
                tools_tracker.edit_tvshow(data)
                data = tools_tracker.load_menu()
            elif cat == "music":
                tools_tracker.edit_music(data)
                data = tools_tracker.load_menu()
            elif cat not in ["movies", "tvshows", "music"]:
                print("Invalid category. Please type Movies, Tv Shows, or Music.")

        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Try again.")

except KeyboardInterrupt:
    print("\n\nForced exit detected. Saving (if needed) and shutting down. Goodbye!")
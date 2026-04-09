import os
import json

def get_path():
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, 'downloads.json')

def init_db():
    path = get_path()

    if not os.path.exists(path):
        initial_data = {
            "media to download": {
                "movies": [],
                "tvshows": [],
                "music": []
            }
        }
        with open('downloads.json', 'w') as f:
            json.dump(initial_data, f, indent=4)
        print("Database created successfully.")
    else:
        print("Database already exists.")

def load_menu():
    path = get_path()
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file is missing, return the empty skeleton
        return {"media to download": {"movies": [], "tvshows": [], "music": []}}


def save_menu(data):
    path = get_path()
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
            print("Data saved successfully!")
    except TypeError:
        print("Error: The data you provided isn't compatible with JSON format.")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

def add_item(data, category, name, year, downloaded=False, seasons=None, album=None):
    clean_category = category.strip().lower().replace(" ", "")
    
    if clean_category not in data["media to download"]:
        print(f"Error: '{clean_category}' is not a valid category.")
        return

    if seasons and clean_category != "tvshows":
        print(f"You cannot add Seasons to the '{clean_category}' category.")
        return
    
    if album and clean_category != "music":
        print(f"You cannot add Album to the '{clean_category}' category.")
        return

    menu_category = data["media to download"][clean_category]

    # check if item exists first
    existing_item = None
    for item in menu_category:
        if item["name"].lower() == name.lower() and item.get("year") == year:
            existing_item = item
            break
    
    # update item
    if existing_item:
        if seasons:
            # check if key exists
            if "seasons" not in existing_item:
                existing_item["seasons"] = {}
            
            # merge new season with existing ones
            existing_item["seasons"].update(seasons)
            print(f"Updated seasons for {name}.")

        if album:
            # check if key exists
            if "album" not in existing_item:
                existing_item["album"] = {}
            
            # add the new album and its status
            existing_item["album"].update(album)
            print(f"Updated album list for {name}.")

    # create item if it doesn't exist
    else:
        new_data = {
            "name": name
        }

        # only add the top-level 'year' if it's not music
        if clean_category != "music":
            new_data["year"] = year
        
        # only add 'downloaded' if it's a movie
        if clean_category == "movies":
            new_data["downloaded"] = downloaded

        # check for option TV info
        if seasons:
            new_data["seasons"] = seasons

        if album:
            new_data["album"] = album

        menu_category.append(new_data)
        print(f"Added new entry: {name}")

    menu_category.sort(key=lambda x: x["name"].lower())
    save_menu(data)

def prompt_back_or_exit():
    while True:
        user_input = input("Type 'back' to go back or 'exit' to exit: ").lower()
        if user_input == 'exit':
            print("\nGoodbye!")
            return "exit"
        elif user_input == 'back':
            return "back"
        else:
            print("Invalid input. Please type 'back' or 'exit'.")

def prompt_filter():
    while True:
        print("\nFilter options:")
        print("1. Show All")
        print("2. Show Downloaded")
        print("3. Show Not Downloaded")
        filter_choice = input("Choose a filter: ").strip()
        if filter_choice in ["1", "2", "3"]:
            return filter_choice
        print("Invalid input. Please choose 1, 2, or 3.")

def edit_item(data, category):
    clean_category = category.strip().lower().replace(" ", "")
    menu_category = data["media to download"][clean_category]

    if len(menu_category) == 0:
        print(f"\nYour {category} list is empty.")
        return

    # show numbered list
    print(f"\n----- {category} -----")
    for i, item in enumerate(menu_category, 1):
        print(f"{i}. {item['name']}")

    # pick an item
    while True:
        raw = input("\nEnter the number of the item to edit or 'back' to go back: ").strip()
        if raw.lower() == 'back':
            return
        if raw.isdigit() and 1 <= int(raw) <= len(menu_category):
            item = menu_category[int(raw) - 1]
            break
        print(f"Invalid input. Please enter a number between 1 and {len(menu_category)}.")

    print(f"\nEditing: {item['name']}")
    return item, menu_category

def edit_movie(data):
    result = edit_item(data, "movies")
    if result is None:
        return
    
    item, menu_category = result

    while True:
        print(f"\n----- Editing: {item['name']} -----")
        print(f"1. Name: {item['name']}")
        print(f"2. Year: {item['year']}")
        print(f"3. Downloaded: {item['downloaded']}")
        print("4. Done editing")

        choice = input("\nWhat would you like to edit?: ").strip()

        if choice == "1":
            new_name = input("Enter new name: ").strip()
            if new_name:
                item['name'] = new_name
                save_menu(data)
                print(f"Name updated to: {new_name}")
            else:
                print("Name cannot be empty.")

        elif choice == "2":
            new_year = input("Enter new year: ").strip()
            if new_year.isdigit():
                item['year'] = new_year
                save_menu(data)
                print(f"Year updated to: {new_year}")
            else:
                print("Invalid year. Please enter numbers only.")

        elif choice == "3":
            while True:
                raw = input("Downloaded? (y/n): ").lower()
                if raw in ['y', 'n']:
                    item['downloaded'] = (raw == 'y')
                    save_menu(data)
                    print(f"Downloaded updated to: {item['downloaded']}")
                    break
                print("Invalid input. Please type 'y' or 'n'.")

        elif choice == "4":
            print("Done editing.")
            break

        else:
            print("Invalid choice. Try again.")

def edit_tvshow(data):
    result = edit_item(data, "tvshows")
    if result is None:
        return
    
    item, menu_category = result

    while True:
        print(f"\n----- Editing: {item['name']} -----")
        print(f"1. Name: {item['name']}")
        print(f"2. Year: {item['year']}")
        print("3. Edit Seasons")
        print("4. Done editing")

        choice = input("\nWhat would you like to edit?: ").strip()

        if choice == "1":
            new_name = input("Enter new name: ").strip()
            if new_name:
                item['name'] = new_name
                save_menu(data)
                print(f"Name updated to: {new_name}")
            else:
                print("Name cannot be empty.")

        elif choice == "2":
            new_year = input("Enter new year: ").strip()
            if new_year.isdigit():
                item['year'] = new_year
                save_menu(data)
                print(f"Year updated to: {new_year}")
            else:
                print("Invalid year. Please enter numbers only.")

        elif choice == "3":
            if "seasons" not in item or len(item["seasons"]) == 0:
                print("No seasons found for this show.")
            else:
                while True:
                    print(f"\n----- Seasons: {item['name']} -----")
                    seasons_list = list(item["seasons"].items())
                    for i, (s_name, s_status) in enumerate(seasons_list, 1):
                        status_text = "Downloaded" if s_status else "Need"
                        print(f"{i}. {s_name}: {status_text}")
                    print("4. Done editing seasons")

                    s_choice = input("\nEnter season number to edit or '4' to go back: ").strip()

                    if s_choice == "4":
                        break
                    elif s_choice.isdigit() and 1 <= int(s_choice) <= len(seasons_list):
                        s_name = seasons_list[int(s_choice) - 1][0]

                        print(f"\n----- Editing: {s_name} -----")
                        print("1. Change downloaded status")
                        print("2. Remove this season")
                        print("3. Back")

                        s_edit = input("\nChoice: ").strip()

                        if s_edit == "1":
                            while True:
                                raw = input(f"Is {s_name} downloaded? (y/n): ").lower()
                                if raw in ['y', 'n']:
                                    item["seasons"][s_name] = (raw == 'y')
                                    save_menu(data)
                                    print(f"{s_name} updated.")
                                    break
                                print("Invalid input. Please type 'y' or 'n'.")

                        elif s_edit == "2":
                            confirm = input(f"Are you sure you want to remove {s_name}? (y/n): ").lower()
                            if confirm == 'y':
                                del item["seasons"][s_name]
                                save_menu(data)
                                print(f"{s_name} removed.")
                                if len(item["seasons"]) == 0:
                                    break
                            else:
                                print("Cancelled.")

                        elif s_edit == "3":
                            continue
                        else:
                            print("Invalid choice. Try again.")
                    else:
                        print(f"Invalid input. Please enter a number between 1 and {len(seasons_list)}.")

        elif choice == "4":
            print("Done editing.")
            break

        else:
            print("Invalid choice. Try again.")

def edit_music(data):
    result = edit_item(data, "music")
    if result is None:
        return
    
    item, menu_category = result

    while True:
        print(f"\n----- Editing: {item['name']} -----")
        print(f"1. Name: {item['name']}")
        print("2. Edit Albums")
        print("3. Done editing")

        choice = input("\nWhat would you like to edit?: ").strip()

        if choice == "1":
            new_name = input("Enter new name: ").strip()
            if new_name:
                item['name'] = new_name
                save_menu(data)
                print(f"Name updated to: {new_name}")
            else:
                print("Name cannot be empty.")

        elif choice == "2":
            if "album" not in item or len(item["album"]) == 0:
                print("No albums found for this artist.")
            else:
                while True:
                    print(f"\n----- Albums: {item['name']} -----")
                    album_list = list(item["album"].items())
                    for i, (a_name, a_info) in enumerate(album_list, 1):
                        status_text = "Downloaded" if a_info["downloaded"] else "Need"
                        print(f"{i}. {a_name} ({a_info['year']}): {status_text}")
                    print(f"{len(album_list) + 1}. Done editing albums")

                    a_choice = input("\nEnter album number to edit or type 'back' to go back: ").strip()

                    if a_choice == str(len(album_list) + 1) or a_choice.lower() == 'back':
                        break
                    elif a_choice.isdigit() and 1 <= int(a_choice) <= len(album_list):
                        a_name = album_list[int(a_choice) - 1][0]
                        a_info = item["album"][a_name]

                        print(f"\n----- Editing: {a_name} -----")
                        print("1. Change album name")
                        print("2. Change album year")
                        print("3. Change downloaded status")
                        print("4. Remove this album")
                        print("5. Back")

                        a_edit = input("\nChoice: ").strip()

                        if a_edit == "1":
                            new_name = input("Enter new album name: ").strip()
                            if new_name:
                                item["album"][new_name] = item["album"].pop(a_name)
                                save_menu(data)
                                print(f"Album renamed to: {new_name}")
                            else:
                                print("Album name cannot be empty.")

                        elif a_edit == "2":
                            new_year = input("Enter new year: ").strip()
                            if new_year.isdigit():
                                a_info["year"] = new_year
                                save_menu(data)
                                print(f"Year updated to: {new_year}")
                            else:
                                print("Invalid year. Please enter numbers only.")

                        elif a_edit == "3":
                            while True:
                                raw = input(f"Is {a_name} downloaded? (y/n): ").lower()
                                if raw in ['y', 'n']:
                                    a_info["downloaded"] = (raw == 'y')
                                    save_menu(data)
                                    print(f"{a_name} updated.")
                                    break
                                print("Invalid input. Please type 'y' or 'n'.")

                        elif a_edit == "4":
                            confirm = input(f"Are you sure you want to remove '{a_name}'? (y/n): ").lower()
                            if confirm == 'y':
                                del item["album"][a_name]
                                save_menu(data)
                                print(f"'{a_name}' removed.")
                                if len(item["album"]) == 0:
                                    break
                            else:
                                print("Cancelled.")

                        elif a_edit == "5":
                            continue
                        else:
                            print("Invalid choice. Try again.")
                    else:
                        print(f"Invalid input. Please enter a number between 1 and {len(album_list)}.")

        elif choice == "3":
            print("Done editing.")
            break

        else:
            print("Invalid choice. Try again.")
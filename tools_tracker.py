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
        if item["name"].lower() == name.lower():
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


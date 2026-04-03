import os
import json

def get_path():
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, 'downloads.json')

def init_db():
    path = get_path()

    if not os.path.exists(path):
        initial_data = {
            "Media To Download": {
                "Movies": [],
                "Tv Shows": [],
                "Music": []
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
        return {"Media To Download": {"Movies": [], "Tv Shows": [], "Music": []}}


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
    clean_category = category.strip().title()
    
    if clean_category not in data["Media To Download"]:
        print(f"Error: '{clean_category}' is not a valid category.")
        return

    if seasons and clean_category != "Tv Shows":
        print(f"You cannot add Seasons to the '{clean_category}' category.")
        return
    
    if album and clean_category != "Music":
        print(f"You cannot add Album to the '{clean_category}' category.")
        return

    menu_category = data["Media To Download"][clean_category]

    # check if item exists first
    existing_item = None
    for item in menu_category:
        if item["Name"].lower() == name.lower():
            existing_item = item
            break
    
    # update item
    if existing_item:
        if seasons:
            # check if key exists
            if "Seasons" not in existing_item:
                existing_item["Seasons"] = {}
            
            # merge new season with existing ones
            existing_item["Seasons"].update(seasons)
            print(f"Updated seasons for {name}.")

        if album:
            # check if key exists
            if "Album" not in existing_item:
                existing_item["Albums"] = {}
            
            # add the new album and its status
            existing_item["Album"].update({album: downloaded})
            print(f"Updated album list for {name}.")

    # create item if it doesn't exist
    else:
        new_data = {
            "Name": name,
            "Year": year,
            "Downloaded": downloaded
        }

        # check for option TV info
        if seasons:
            new_data["Seasons"] = seasons

        if album:
            new_data["Album"] = {album: downloaded}

    menu_category.append(new_data)
    menu_category.sort(key=lambda x: x["Name"].lower())
    save_menu(data)


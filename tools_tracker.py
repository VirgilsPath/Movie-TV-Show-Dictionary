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
                "TV Shows": [],
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
        return {"Media To Download": {"Movies": [], "TV Shows": [], "Music": []}}


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

def add_item(data, category, name, year, downloaded=False):
    clean_category = category.strip().title()
    if clean_category not in data["Media To Download"]:
        print(f"Error: '{clean_category}' is not a valid category.")
        return

    menu_category = data["Media To Download"][clean_category]

    new_data = {
        "Name": name,
        "Year": year,
        "Downloaded": downloaded
    }
    menu_category.append(new_data)
    menu_category.sort(key=lambda x: x["Name"].lower())
    save_menu(data)


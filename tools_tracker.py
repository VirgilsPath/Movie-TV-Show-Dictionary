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

# need to make a load function
# need to make a save function
# need to make a add_item function

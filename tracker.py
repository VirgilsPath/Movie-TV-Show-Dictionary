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

init_db()
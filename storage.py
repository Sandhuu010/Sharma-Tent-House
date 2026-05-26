import json
import os

FILE_PATH = "data/items.json"


def load_items():
    # Create file if missing
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as file:
            json.dump([], file)

    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Error: items.json is corrupted.")
        return []


def save_items(items):
    with open(FILE_PATH, "w") as file:
        json.dump(items, file, indent=4)
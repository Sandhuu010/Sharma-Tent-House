import json
import os


def load_data(file_path):

    # Create file if missing
    if not os.path.exists(file_path):

        with open(file_path, "w") as file:
            json.dump([], file)

    try:

        with open(file_path, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:

        print(f"Error: {file_path} contains invalid JSON.")

        return []


def save_data(file_path, data):

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
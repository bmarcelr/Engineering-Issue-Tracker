import json

def load_data(file_path="data/issues.json"):
    with open(file_path, "r") as file:
        return json.load(file)

def save_data(tracker_data, file_path="data/issues.json"):
    with open(file_path, "w") as file:
        json.dump(tracker_data, file, indent=4)
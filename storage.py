
import json
import os

SAVE_PATH = "scrolls_data.json"

def save_message(entry):
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_messages():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r") as f:
            return json.load(f)
    return []

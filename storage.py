import json
import os
from datetime import datetime

DATA_FILE = "scrolls_data.json"

def save_message(name, message, category="Message"):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "name": name or "Anonymous",
        "category": category,
        "message": message
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_messages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []
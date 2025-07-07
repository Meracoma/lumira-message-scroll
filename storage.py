# storage.py

import json
from datetime import datetime
import os

# Path to the scroll data file
DATA_FILE = "scrolls_data.json"

def save_message(name, message, category="General"):
    """
    Save a scroll/message to the local JSON file.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "name": name or "Anonymous",
        "category": category,
        "message": message
    }

    # Load existing messages if the file exists
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Add new entry and save
    data.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_messages():
    """
    Load all saved messages from the JSON file.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return []# Storage functions for messages and image paths

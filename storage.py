import json
from datetime import datetime

SCROLLS_FILE = "data/scrolls.json"

def save_message(user, message):
    scrolls = load_messages()
    entry = {
        "user": user or "Anonymous",
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    scrolls.append(entry)
    with open(SCROLLS_FILE, "w") as f:
        json.dump(scrolls, f, indent=2)

def load_messages():
    try:
        with open(SCROLLS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

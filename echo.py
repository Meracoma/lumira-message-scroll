# echo.py

import os
import json
from datetime import datetime

ECHO_FILE = os.path.join("data", "echoes.json")

def tag_echo(name, message, tag):
    """Save a message with an echo tag."""
    if not os.path.exists("data"):
        os.makedirs("data")

    echo_entry = {
        "name": name or "Anonymous",
        "message": message.strip(),
        "tag": tag.strip(),
        "timestamp": datetime.now().isoformat()
    }

    # Load existing echoes
    echoes = []
    if os.path.exists(ECHO_FILE):
        with open(ECHO_FILE, "r", encoding="utf-8") as f:
            echoes = json.load(f)

    # Add and save
    echoes.append(echo_entry)
    with open(ECHO_FILE, "w", encoding="utf-8") as f:
        json.dump(echoes, f, indent=2)

def list_echoes():
    """Return a list of all echo-tagged entries."""
    if os.path.exists(ECHO_FILE):
        with open(ECHO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

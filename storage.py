# storage.py

import os
import json
from datetime import datetime
import uuid
import shutil

DATA_FILE = os.path.join("data", "scrolls.json")
IMAGE_FOLDER = os.path.join("data", "images")

def save_message(entry, image_file=None):
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    # Handle image saving
    if image_file is not None:
        ext = os.path.splitext(image_file.name)[1]
        filename = f"{uuid.uuid4()}{ext}"
        image_path = os.path.join(IMAGE_FOLDER, filename)
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())
        entry["image_path"] = image_path
    else:
        entry["image_path"] = None

    # Load existing entries
    entries = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            entries = json.load(f)

    entries.append(entry)

    # Save back
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

def load_messages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

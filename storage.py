# === 💾 LUMIRA MEMORY STORAGE SYSTEM (storage.py) ===

import os
import json
from datetime import datetime

# === 🔖 Constants ===
STORAGE_DIR = "scroll_memory"
SCROLL_FILE = os.path.join(STORAGE_DIR, "scrolls.json")

# === ✅ Ensure the memory folder exists
os.makedirs(STORAGE_DIR, exist_ok=True)


# === 💾 Save Message Scroll ===
def save_message(scroll, tag=None, favorite=False, echo_log=False):
    """Append a new scroll to storage with optional tag + metadata."""
    data = load_messages()

    scroll_entry = {
        "message": scroll,
        "timestamp": datetime.utcnow().isoformat(),
        "tag": tag or None,
        "favorite": favorite,
        "echo_log": echo_log,
    }

    data.append(scroll_entry)

    with open(SCROLL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[MemoryLog] Saved scroll: {scroll_entry}")  # 🧠 For Phase 3 Echo Streams


# === 📖 Load All Messages ===
def load_messages():
    """Load all stored scrolls."""
    if os.path.exists(SCROLL_FILE):
        with open(SCROLL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# === 🌟 Get All Favorites ===
def load_favorites():
    """Load only starred scrolls."""
    return [s for s in load_messages() if s.get("favorite")]


# === 🧠 Get All Echo-Logged Messages ===
def load_echo_logs():
    """Load scrolls marked for echo log."""
    return [s for s in load_messages() if s.get("echo_log")]


# === 🧹 Optional: Reset / Clear Scrolls (use with caution) ===
def clear_scrolls():
    if os.path.exists(SCROLL_FILE):
        os.remove(SCROLL_FILE)

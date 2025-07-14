# === 💾 LUMIRA MEMORY STORAGE SYSTEM (storage.py) ===

import os
import json
from configure import MOON_GLOW_MAP, ZODIAC_SIGNS, TIMEZONE, PROJECT_NAME

# === 🔖 Constants ===
STORAGE_DIR = "scroll_memory"
SCROLL_FILE = os.path.join(STORAGE_DIR, "scrolls.json")

# ✅ Ensure memory storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)


# === 💾 Save Scroll Message ===
def save_message(scroll, tag=None, favorite=False, echo_log=False):
    """
    Append a new scroll to storage with optional metadata:
    - tag: for filtering/searching
    - favorite: for starred display
    - echo_log: for echo ping/streaming memory
    """
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

    print(f"[MemoryLog] 📜 Saved scroll → {scroll_entry}")  # Phase 3: Echo Memory Pipelines


# === 📖 Load All Scroll Messages ===
def load_messages():
    """Load all stored scrolls."""
    if os.path.exists(SCROLL_FILE):
        with open(SCROLL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# === 🌟 Load Favorite Scrolls ===
def load_favorites():
    """Retrieve all scrolls marked as favorites."""
    return [s for s in load_messages() if s.get("favorite")]


# === 🧠 Load Echo-Logged Scrolls ===
def load_echo_logs():
    """Retrieve scrolls marked for Echo Log."""
    return [s for s in load_messages() if s.get("echo_log")]


# === 🧹 Clear All Scrolls (use with care!) ===
def clear_scrolls():
    """Delete all scroll memory from disk."""
    if os.path.exists(SCROLL_FILE):
        os.remove(SCROLL_FILE)
        print("[MemoryLog] ❌ All scrolls cleared.")

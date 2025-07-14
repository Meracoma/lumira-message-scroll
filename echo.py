# === 🧠 LUMIRA ECHO SYSTEM (echo.py) ===

import os
import json
from datetime import datetime
from typing import Optional, List, Dict


# === 📂 ECHO STORAGE CONFIG ===

ECHO_DIR = "data"
ECHO_FILE = os.path.join(ECHO_DIR, "echoes.json")


# === 🛠️ ECHO FILE SETUP ===

def ensure_echo_storage():
    """Ensure echo storage folder and file exist."""
    if not os.path.exists(ECHO_DIR):
        os.makedirs(ECHO_DIR)
    if not os.path.exists(ECHO_FILE):
        with open(ECHO_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


# === 📥 LOAD + SAVE CORE ===

def load_echoes() -> List[Dict]:
    """Load all stored echoes."""
    ensure_echo_storage()
    with open(ECHO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_echoes(echoes: List[Dict]):
    """Save all echoes to disk (overwrite full list)."""
    with open(ECHO_FILE, "w", encoding="utf-8") as f:
        json.dump(echoes, f, indent=2)


# === 🧠 TAGGING + MEMORY PING ===

def tag_echo(name: str, message: str, tag: str, echo_type: Optional[str] = None, extra: Optional[Dict] = None):
    """
    Tag and save a scroll/message into Echo memory.

    Args:
        name: Who the scroll came from.
        message: The scroll contents.
        tag: Echo category (e.g., HUM_BODY, DREAM_SEED).
        echo_type: Optional sub-classifier (e.g., log, memory, ping).
        extra: Any extra metadata or origin info.
    """
    ensure_echo_storage()

    echo_entry = {
        "name": name.strip() or "Anonymous",
        "message": message.strip(),
        "tag": tag.strip(),
        "type": echo_type or "log",
        "timestamp": datetime.utcnow().isoformat(),
        "extra": extra or {}
    }

    echoes = load_echoes()
    echoes.append(echo_entry)
    save_echoes(echoes)

    print(f"[ECHO] Saved: {tag} → {name} → {echo_type or 'log'}")


# === 📋 LIST + FILTER UTILS ===

def list_echoes(tag_filter: Optional[str] = None) -> List[Dict]:
    """Return all echoes or only those with a matching tag."""
    echoes = load_echoes()
    if tag_filter:
        result = [e for e in echoes if e["tag"].strip().lower() == tag_filter.strip().lower()]
        print(f"[ECHO] Filter by tag: {tag_filter} → {len(result)} match(es)")
        return result
    print(f"[ECHO] Loaded all echoes → {len(echoes)} total")
    return echoes


def recent_echoes(limit: int = 10) -> List[Dict]:
    """Return most recent echoes (sorted descending by time)."""
    echoes = load_echoes()
    result = sorted(echoes, key=lambda e: e["timestamp"], reverse=True)[:limit]
    print(f"[ECHO] Recent echoes pulled → {len(result)} shown")
    return result

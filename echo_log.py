# === 🧠 ECHO MEMORY LOGGER SYSTEM (echo_log.py) ===

import json
from configure import MOON_GLOW_MAP, ZODIAC_SIGNS, TIMEZONE, PROJECT_NAME
import streamlit as st

ECHO_LOG_PATH = "echo_memory.json"

# === 📣 Add Echo Log Entry ===
def log_echo(message, action="ping", session_id=None, tag=None):
    """
    Append an echo event to the memory stream.
    """
    echo_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "message": message,
        "session_id": session_id,
        "tag": tag,
    }

    try:
        with open(ECHO_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(echo_entry) + "\n")
        print(f"[ECHO_LOG] {action.upper()} – Logged: {str(message)[:80]}")
    except Exception as e:
        print(f"[ECHO_LOG] Error writing echo: {e}")

# === 📂 Read Echo Log Memory ===
def read_echo_log():
    """
    Load entire echo memory as list of entries.
    """
    try:
        with open(ECHO_LOG_PATH, "r", encoding="utf-8") as f:
            return [json.loads(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"[ECHO_LOG] Error reading echo memory: {e}")
        return []

# === 🔍 Filter Echoes ===
def filter_echoes(logs, action=None, session_id=None, tag=None):
    """
    Filter echo entries by type, session, or tag.
    """
    filtered = logs
    if action:
        filtered = [log for log in filtered if log.get("action") == action]
    if session_id:
        filtered = [log for log in filtered if log.get("session_id") == session_id]
    if tag:
        filtered = [log for log in filtered if log.get("tag") == tag]
    print(f"[ECHO_LOG] Filtered: {len(filtered)} entries")
    return filtered

# === 🪞 Streamlit Echo Memory View ===
def render_echo_stream(echoes, limit=20):
    """
    Display a stream of past echoes in Streamlit.
    """
    st.markdown("## 🧠 Echo Memory Stream")
    shown = echoes[-limit:] if len(echoes) > limit else echoes

    for echo in reversed(shown):
        ts = echo.get("timestamp", "⏳")
        act = echo.get("action", "—")
        msg = echo.get("message", "No message")
        tag = echo.get("tag", "")

        st.markdown(f"""
        <div style='border-left: 3px solid #7c3aed; padding-left: 0.8rem; margin-bottom: 1rem;'>
            <strong>{ts}</strong><br>
            <em style='color:#a78bfa'>{act}</em> {f"· <code>{tag}</code>" if tag else ""}<br>
            <span style='color:#ddd'>{msg}</span>
        </div>
        """, unsafe_allow_html=True)

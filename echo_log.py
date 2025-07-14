# === 📣 ECHO LOGGER SYSTEM (echo_log.py) ===

import json
from datetime import datetime
import streamlit as st

ECHO_LOG_PATH = "echo_memory.json"

def log_echo(message, action="ping", session_id=None, tag=None):
    """
    Append an echo log entry to the echo memory.
    - message: the content (str or dict)
    - action: e.g. 'favorited', 'filter_applied'
    - session_id: optional user/session ID
    - tag: optional echo tag (e.g. HUM_BODY)
    """
    echo_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "message": message,
        "session_id": session_id,
        "tag": tag
    }
    try:
        with open(ECHO_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(echo_entry) + "\n")
        print(f"[EchoLog] {action.upper()} — {message}")
    except Exception as e:
        print(f"[EchoLog] Failed to write echo: {e}")

def read_echo_log():
    """
    Load full echo memory log.
    Returns list of dicts.
    """
    try:
        with open(ECHO_LOG_PATH, "r", encoding="utf-8") as f:
            return [json.loads(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"[EchoLog] Failed to read echo log: {e}")
        return []

def filter_echoes(logs, action=None, session_id=None, tag=None):
    """
    Filter echo logs by action, session ID, or tag.
    """
    filtered = logs
    if action:
        filtered = [log for log in filtered if log.get("action") == action]
    if session_id:
        filtered = [log for log in filtered if log.get("session_id") == session_id]
    if tag:
        filtered = [log for log in filtered if log.get("tag") == tag]
    return filtered

def render_echo_stream(echoes, limit=20):
    """
    Visual stream view of echo memory.
    Renders in Streamlit.
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

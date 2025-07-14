# === 📣 ECHO LOGGER (echo_log.py) ===

import json
from datetime import datetime

ECHO_LOG_PATH = "echo_memory.json"

def log_echo(message, action="ping"):
    echo_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "message": message
    }
    try:
        with open(ECHO_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(echo_data) + "\n")
    except Exception as e:
        print(f"[EchoLog] Failed to write echo: {e}")

def read_echo_log():
    try:
        with open(ECHO_LOG_PATH, "r", encoding="utf-8") as f:
            return [json.loads(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"[EchoLog] Failed to read echo log: {e}")
        return []

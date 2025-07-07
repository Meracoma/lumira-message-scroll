
# echo.py

def generate_echo_response(message, mode="poetic"):
    if mode == "poetic":
        return f"✨ A whisper returns: '{message}' — remembered by the scroll."
    elif mode == "narrative":
        return f"📖 Echo retrieved: Once, someone left behind this thought — '{message}'."
    else:
        return f"Echo: {message}"

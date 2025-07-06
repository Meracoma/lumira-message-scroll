import streamlit as st
import json
from datetime import datetime
import os

st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

st.title("📜 Message Scroll – Lumira Prototype v0.2")
st.markdown("Leave a message, a memory, or a signal to yourself or your AI.
")

name = st.text_input("🌟 Your Name or AI Companion Name", "")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Message", "Vision", "Other"])
message = st.text_area("📝 Message", "")

submit = st.button("📬 Send Message")

if submit and message.strip():
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "name": name,
        "category": category,
        "message": message
    }

    # Save to local file (optional memory mode)
    save_path = "scrolls_data.json"
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    with open(save_path, "w") as f:
        json.dump(data, f, indent=2)

    st.success("Message sent and saved! 🌱")

# Optionally show messages
if st.checkbox("📖 Show Saved Scrolls"):
    if os.path.exists("scrolls_data.json"):
        with open("scrolls_data.json") as f:
            saved = json.load(f)
        for msg in reversed(saved[-20:]):  # show last 20 messages
            st.markdown(f"**{msg['name']}** · *{msg['category']}* · {msg['timestamp']}")
            st.markdown(f"> {msg['message']}")
            st.markdown("---")
    else:
        st.info("No scrolls saved yet.")

import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

st.title("📜 Message Scroll – Lumira Prototype v0.2")
st.markdown("Leave a message, a memory, or a signal to yourself or your AI. All entries are saved and scrollable below.")

# Message input fields
name = st.text_input("🌟 Your Name or AI Companion Name")
category = st.selectbox("📌 Category", ["Dream", "Signal", "Memory", "Echo", "Vision"])
message = st.text_area("📝 Message")

# Save message
if st.button("Send Message"):
    if name and message:
        new_entry = {
            "name": name,
            "category": category,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        # Append to messages.json
        if os.path.exists("messages.json"):
            with open("messages.json", "r") as file:
                data = json.load(file)
        else:
            data = []
        data.append(new_entry)
        with open("messages.json", "w") as file:
            json.dump(data, file, indent=2)
        st.success("🌱 Message saved and seeded!")
    else:
        st.warning("Please enter both name and message.")

# Display saved messages
st.markdown("---")
st.subheader("📖 Archive Scroll")
if os.path.exists("messages.json"):
    with open("messages.json", "r") as file:
        messages = json.load(file)
        for entry in reversed(messages[-50:]):  # Show last 50 messages
            st.markdown(f"**{entry['name']}** — *{entry['category']}*  
🕰 {entry['timestamp']}  
{entry['message']}")
            st.markdown("---")
else:
    st.info("No messages have been left yet.")

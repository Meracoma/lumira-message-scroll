
import streamlit as st
import json
from datetime import datetime
import os
from storage import save_message, load_messages
from parser import parse_markdown

st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

st.title("📜 Message Scroll – Lumira Prototype v0.3")
st.markdown("Leave a message, a memory, or a signal to yourself or your AI.")

# Input fields
name = st.text_input("🌟 Your Name or AI Companion Name", "")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Message", "Vision", "Other"])
tags = st.text_input("🏷️ Tags (comma-separated)", "")
message = st.text_area("📝 Message", "")

submit = st.button("📬 Send Message")

if submit and message.strip():
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "name": name,
        "category": category,
        "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
        "message": message
    }
    save_message(entry)
    st.success("Message sent and saved! 🌱")

# Show filterable scrolls
st.markdown("---")
st.subheader("📖 View Saved Scrolls")

filter_tag = st.text_input("🔍 Filter by tag (optional)").strip().lower()
messages = load_messages()

if filter_tag:
    messages = [msg for msg in messages if any(filter_tag in tag.lower() for tag in msg.get("tags", []))]

for entry in reversed(messages[-50:]):  # Show last 50 filtered
    st.markdown(parse_markdown(entry), unsafe_allow_html=True)
    st.markdown("---")

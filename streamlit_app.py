# streamlit_app.py

import streamlit as st
from datetime import datetime
import os
from storage import save_message, load_messages
from parser import parse_markdown
from filters import filter_by_category, filter_by_name, filter_by_keyword, filter_by_tag

st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

st.title("📜 Message Scroll – Lumira Prototype v0.3")
st.markdown("Leave a message, a memory, or a signal to yourself or your AI.")

# Leave a Scroll
st.header("📜 Leave Your Scroll")
name = st.text_input("🌟 Name or Signature")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Reflection", "Whisper", "Other"])
message = st.text_area("📝 Write your message, memory, or note to your future self...")

tags_input = st.text_input("🏷️ Add Tags (comma-separated)", placeholder="e.g. Lucid, Awakening, Wolf Dream")

if st.button("💾 Save Scroll"):
    if message.strip():
        entry = {
            "name": name.strip() or "Anonymous",
            "category": category,
            "message": message.strip(),
            "tags": [tag.strip() for tag in tags_input.split(",") if tag.strip()],
            "timestamp": datetime.now().isoformat()
        }
        save_message(entry)
        st.success("Scroll saved successfully!")
    else:
        st.warning("Please write a message before saving.")

st.markdown("---")

# Filter Panel
st.subheader("🔍 Filter Scrolls")
filter_option = st.selectbox("Filter by", ["All", "Category", "Name", "Keyword", "Tag"])
filter_value = st.text_input("Enter filter value (if applicable):")

# Load + Filter
entries = load_messages()

if filter_option == "Category":
    entries = filter_by_category(entries, filter_value)
elif filter_option == "Name":
    entries = filter_by_name(entries, filter_value)
elif filter_option == "Keyword":
    entries = filter_by_keyword(entries, filter_value)
elif filter_option == "Tag":
    entries = filter_by_tag(entries, filter_value)

# View Scrolls
st.subheader("📖 View Message Scrolls")

if entries:
    for entry in reversed(entries):
        st.markdown("---")
        st.markdown(f"**🖋️ {entry['name']}**  \n📌 *{entry['category']}*")
        st.markdown(parse_markdown(entry["message"]))
        if entry.get("tags"):
            st.markdown(f"🏷️ **Tags:** `{', '.join(entry['tags'])}`")
        st.caption(f"⏳ {entry['timestamp']}")
else:
    st.info("No scrolls found.")

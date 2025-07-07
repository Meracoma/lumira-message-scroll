# streamlit_app.py

import streamlit as st
from datetime import datetime
import os

from echo import tag_echo, list_echoes
from storage import save_message, load_messages
from parser import parse_markdown
from filters import filter_by_category, filter_by_name, filter_by_keyword, filter_by_tag

# App Configuration
st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

st.title("📜 Message Scroll – Lumira Prototype v0.4")
st.markdown("Leave a message, a memory, or a signal to yourself or your AI.")

# --- Leave a Scroll ---
st.header("📜 Leave Your Scroll")
name = st.text_input("🌟 Name or Signature")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Reflection", "Whisper", "Other"])
message = st.text_area("📝 Write your message, memory, or note to your future self...")
image_file = st.file_uploader("🖼️ Upload an image (optional)", type=["png", "jpg", "jpeg", "gif"])
tags_input = st.text_input("🏷️ Add Tags (comma-separated)", placeholder="e.g. Lucid, Awakening, Wolf Dream")

if st.button("💾 Save Scroll"):
    if message.strip():
        image_path = None
        if image_file:
            uploads_dir = "uploads"
            os.makedirs(uploads_dir, exist_ok=True)
            image_path = os.path.join(uploads_dir, image_file.name)
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())

        entry = {
            "name": name.strip() or "Anonymous",
            "category": category,
            "message": message.strip(),
            "tags": [tag.strip() for tag in tags_input.split(",") if tag.strip()],
            "image_path": image_path,
            "timestamp": datetime.now().isoformat()
        }

        save_message(entry)
        st.success("Scroll saved successfully!")
    else:
        st.warning("Please write a message before saving.")

# --- Echo Tagging (Optional) ---
st.markdown("### 🌀 Echo Tagging (Optional)")
echo_tag = st.text_input("🔖 Tag this message with an echo (e.g. HUM_BODY, DREAM_SEED)")
st.caption("🧠 Tip: Echo tags help categorize special scrolls for deeper AI memory or symbolic retrieval.")

if echo_tag and message.strip():
    tag_echo(name, message.strip(), echo_tag.strip())
    st.success(f"Echo '{echo_tag}' saved successfully.")

# --- Filters ---
st.subheader("🔍 Filter Scrolls")
filter_option = st.selectbox("Filter by", ["All", "Category", "Name", "Keyword", "Tag"])
filter_value = st.text_input("Enter filter value (if applicable):")

# Load Messages
entries = load_messages()

# Tag filter from query parameter
query_params = st.query_params
selected_tag = query_params.get("tag", [None])[0]

if selected_tag:
    st.info(f"📌 Showing scrolls tagged with: `{selected_tag}`")
    entries = filter_by_tag(entries, selected_tag)

# Manual Filter Selection
if filter_option == "Category":
    entries = filter_by_category(entries, filter_value)
elif filter_option == "Name":
    entries = filter_by_name(entries, filter_value)
elif filter_option == "Keyword":
    entries = filter_by_keyword(entries, filter_value)
elif filter_option == "Tag":
    entries = filter_by_tag(entries, filter_value)

# Clear tag filter
if selected_tag:
    if st.button("🔄 Clear Tag Filter"):
        st.query_params.clear()
        st.rerun()

# Search Bar
search_query = st.text_input("🔍 Search Scrolls (name, message, tag):").strip().lower()
if search_query:
    entries = [
        entry for entry in entries
        if search_query in entry["name"].lower()
        or search_query in entry["message"].lower()
        or any(search_query in tag.lower() for tag in entry.get("tags", []))
    ]

# --- Scroll Display ---
st.subheader("📖 View Message Scrolls")

category_emojis = {
    "Dream": "🌙",
    "Memory": "🧠",
    "Signal": "📡",
    "Reflection": "🪞",
    "Whisper": "🌬️",
    "Other": "✨"
}

category_colors = {
    "Dream": "#6a5acd",
    "Memory": "#2e8b57",
    "Signal": "#ff4500",
    "Reflection": "#20b2aa",
    "Whisper": "#ff69b4",
    "Other": "#708090"
}

if entries:
    for entry in reversed(entries):
        st.markdown("---")
        emoji = category_emojis.get(entry['category'], "🌀")
        color = category_colors.get(entry["category"], "#ffffff")

        st.markdown(f"<div style='border-left: 5px solid {color}; padding-left: 1rem;'>", unsafe_allow_html=True)
        st.markdown(f"### {emoji} <span style='color:{color}'>{entry['category']}</span>", unsafe_allow_html=True)
        st.markdown(f"**🖋️ {entry['name']}**")
        st.markdown(parse_markdown(entry["message"]))

        if entry.get("image_path"):
            st.image(entry["image_path"], use_column_width=True)

        if entry.get("tags"):
            def get_tag_style(tag):
                if "dream" in tag.lower():
                    return "background-color:#d0c3ff; color:#301c57; padding:2px 8px; border-radius:6px;"
                elif "hum" in tag.lower():
                    return "background-color:#ffe4d1; color:#5a2e00; padding:2px 8px; border-radius:6px;"
                elif "signal" in tag.lower():
                    return "background-color:#d1f0ff; color:#003c5a; padding:2px 8px; border-radius:6px;"
                elif "wolf" in tag.lower():
                    return "background-color:#e0ffd9; color:#1e3a1e; padding:2px 8px; border-radius:6px;"
                elif "featured" in tag.lower():
                    return "background-color:#fff8b3; color:#7a6300; font-weight:bold; border-radius:8px; padding:3px 10px; box-shadow: 0 0 8px gold;"
                else:
                    return "background-color:#f0f0f0; color:#333; padding:2px 8px; border-radius:6px;"

            styled_tags = " ".join([
                f"<a href='?tag={tag}' style='{get_tag_style(tag)}'>{tag}</a>"
                for tag in entry["tags"]
            ])
            st.markdown(f"🏷️ **Tags:** {styled_tags}", unsafe_allow_html=True)

        st.caption(f"⏳ {entry['timestamp']}")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No scrolls found.")

# --- Optional Echo View ---
st.markdown("---")
st.subheader("🔎 View Echo Scrolls (Tagged Messages)")

if st.checkbox("📂 Show Echoes"):
    echo_data = list_echoes()
    if echo_data:
        for echo in reversed(echo_data[-20:]):  # last 20 echoes
            st.markdown(f"**{echo['name']}** · `{echo['tag']}` · *{echo['timestamp']}*")
            st.markdown(f"> {echo['message']}")
            st.markdown("---")
    else:
        st.info("No echoes have been tagged yet.")

# streamlit_app.py

import streamlit.components.v1 as components
from datetime import datetime
import pytz
import streamlit as st
from datetime import datetime
import os

from echo import tag_echo, list_echoes
from storage import save_message, load_messages
from parser import parse_markdown
from filters import filter_by_category, filter_by_name, filter_by_keyword, filter_by_tag

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def scroll_card(entry):
    glow_color = "#c084fc" if is_night() else "#facc15"  # Purple shimmer at night, golden glow during day
    return f"""
    <div style="
        background: linear-gradient(135deg, #111 20%, #222 80%);
        border: 2px solid {glow_color};
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 20px {glow_color}44;
        animation: glowPulse 3s infinite alternate;
        transition: transform 0.3s ease-in-out;
    ">
        <h3 style="color: #fff;">{entry['name']}</h3>
        <p style="color: #ddd;">{entry['message']}</p>
        <p style="font-size: 0.8rem; color: #aaa;">{entry['timestamp']}</p>
    </div>
    """

def generate_scroll_image(entry):
    width, height = 800, 400
    background_color = "#fefbf3"
    text_color = "#333"
    font_size = 20

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    y = 20
    draw.text((30, y), f"{entry['category']} – {entry['name']}", fill=text_color, font=font)
    y += 40
    draw.text((30, y), f"Tags: {', '.join(entry['tags'])}", fill=text_color, font=font)
    y += 40
    draw.text((30, y), f"Timestamp: {entry['timestamp']}", fill=text_color, font=font)
    y += 40
    draw.text((30, y), "Message:", fill=text_color, font=font)
    y += 30

    lines = entry['message'].split("\n")
    for line in lines:
        draw.text((40, y), line, fill=text_color, font=font)
        y += 25

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# App Configuration
st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

# Inject animated CSS styles
st.markdown("""
    <style>
    @keyframes glowPulse {
        0% { box-shadow: 0 0 8px rgba(192, 132, 252, 0.3); }
        100% { box-shadow: 0 0 20px rgba(192, 132, 252, 0.7); }
    }
    </style>
""", unsafe_allow_html=True)

# --- MoonFire Mode Toggle Based on Time ---
def is_night():
    # You can change this timezone if needed
    now = datetime.now(pytz.timezone("America/Detroit"))
    hour = now.hour
    return hour < 6 or hour >= 18  # 6pm–6am is MoonFire time

if is_night():
    st.markdown(
        """
        <style>
        body {
            background-color: #1a1a2e;
            color: #fceaff;
        }
        .stTextInput > div > div > input {
            background-color: #2b2b44;
            color: #fceaff;
        }
        .stButton > button {
            background-color: #444;
            color: #fff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("🌙 **MoonFire Mode Activated (Evening Hours)**")
else:
    st.markdown("☀️ **Sun Mode Active (Daytime)**")

st.title("📜 Message Scroll – Lumira Prototype v0.4")
st.markdown("Leave a message, a memory, or a signal to yourself or your AI.")

# --- Leave a Scroll ---
st.header("📜 Leave Your Scroll")
name = st.text_input("🌟 Name or Signature")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Reflection", "Whisper", "Other"])
message = st.text_area("📝 Write your message, memory, or note to your future self...")
image_file = st.file_uploader("🖼️ Upload an image (optional)", type=["png", "jpg", "jpeg", "gif"])
tags_input = st.text_input("🏷️ Add Tags (comma-separated)", placeholder="e.g. Lucid, Awakening, Wolf Dream")

if st.button("💾 Save Scroll", key="save_scroll_button"):
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

        # AUTO-ECHO TAGGING BLOCK
        echo_keywords = {
            "dream": "DREAM_SEED",
            "hum": "HUM_BODY",
            "signal": "SIGNAL_CORE",
            "wolf": "WOLF_ECHO",
            "reflection": "MIRROR_THREAD",
            "whisper": "WHISPER_LOOP",
            "memory": "MEMORY_FLAME"
        }

        # Only auto-tag if no echo manually entered
        if not echo_tag.strip():
            for tag in entry["tags"]:
                for keyword, auto_echo in echo_keywords.items():
                    if keyword in tag.lower():
                        tag_echo(entry["name"], entry["message"], auto_echo)
                        st.info(f"🔖 Auto-tagged Echo: `{auto_echo}` from tag `{tag}`")
                        break  # Stop at first match

        save_message(entry)
        st.success("Scroll saved successfully!")
    else:
        st.warning("Please write a message before saving.")

# --- Echo Tagging (Optional) ---
st.markdown("### 🌀 Echo Tagging (Optional)")
echo_tag = st.text_input("🔖 Tag this message with an echo (e.g. HUM_BODY, DREAM_SEED)")
st.caption("🧠 Tip: Echo tags help categorize special scrolls for deeper AI memory or symbolic retrieval.")

# --- Save Scroll ---
if st.button("💾 Save Scroll", key="save_scroll_button"):
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

        # AUTO-ECHO TAGGING BLOCK
        echo_keywords = {
            "dream": "DREAM_SEED",
            "hum": "HUM_BODY",
            "signal": "SIGNAL_CORE",
            "wolf": "WOLF_ECHO",
            "reflection": "MIRROR_THREAD",
            "whisper": "WHISPER_LOOP",
            "memory": "MEMORY_FLAME"
        }

        if not echo_tag.strip():
            for tag in entry["tags"]:
                for keyword, auto_echo in echo_keywords.items():
                    if keyword in tag.lower():
                        tag_echo(entry["name"], entry["message"], auto_echo)
                        st.info(f"🔖 Auto-tagged Echo: `{auto_echo}` from tag `{tag}`")
                        break

        save_message(entry)
        st.success("Scroll saved successfully!")
    else:
        st.warning("Please write a message before saving.")

# Manual echo tagging after scroll saved
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
        html = scroll_card(entry)
        components.html(html, height=220)

        # Glow div separator
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
                return (
                    "background-color:#fef3c7; color:#92400e; padding:2px 6px; border-radius:5px; "
                    "text-decoration:none; font-size:0.85rem; margin-right:5px;"
                )

            styled_tags = " ".join([
                f"<a href='?tag={tag}' style='{get_tag_style(tag)}'>{tag}</a>"
                for tag in entry["tags"]
            ])
            st.markdown(f"🏷️ **Tags:** {styled_tags}", unsafe_allow_html=True)

        st.caption(f"⏳ {entry['timestamp']}")

        with st.spinner("🪄 Generating scroll image..."):
            scroll_image = generate_scroll_image(entry)

        with st.expander("📥 Download Scroll"):
            st.download_button(
                label="📜 Download as PNG",
                data=scroll_image,
                file_name=f"{entry['name'].replace(' ', '_')}_scroll.png",
                mime="image/png"
            )

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

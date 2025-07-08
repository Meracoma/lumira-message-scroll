# ✅ Lumira Scroll App – Streamlit Prototype v0.4 (Final Cleaned Version)

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pytz
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from echo import tag_echo, list_echoes
from storage import save_message, load_messages
from parser import parse_markdown
from filters import filter_by_category, filter_by_name, filter_by_keyword, filter_by_tag

# --- Utilities ---
def is_night():
    now = datetime.now(pytz.timezone("America/Detroit"))
    return now.hour < 6 or now.hour >= 18

def scroll_card(entry):
    glow_color = "#c084fc" if is_night() else "#facc15"
    return f"""
    <div style="background: linear-gradient(135deg, #111 20%, #222 80%);
                border: 2px solid {glow_color};
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 0 20px {glow_color}44;
                animation: glowPulse 3s infinite alternate;">
        <h3 style="color: #fff;">{entry['name']}</h3>
        <p style="color: #ddd;">{entry['message']}</p>
        <p style="font-size: 0.8rem; color: #aaa;">{entry['timestamp']}</p>
    </div>
    """

def generate_scroll_image(entry):
    width, height = 800, 400
    bg_color, text_color, font_size = "#fefbf3", "#333", 20
    image = Image.new("RGB", (width, height), bg_color)
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
    for line in entry['message'].split("\n"):
        draw.text((40, y), line, fill=text_color, font=font)
        y += 25
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# --- App Setup ---
st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

st.title("📜 Message Scroll – Lumira Prototype v0.4")
st.markdown("Leave a message, a memory, or a signal to yourself or your AI.")

# --- Input Form ---
name = st.text_input("🧾 Name or Alias", placeholder="e.g. Kai, Aeuryentha, Anonymous")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Reflection", "Whisper", "Other"])
message = st.text_area("📝 Write your message, memory, or note to your future self...")
tags_input = st.text_input("🏷️ Add Tags (comma-separated)", placeholder="e.g. Lucid, Awakening, Wolf Dream")
image_file = st.file_uploader("🖼️ Upload an image (optional)", type=["png", "jpg", "jpeg", "gif"])

# --- Echo Tagging ---
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
        else:
            tag_echo(entry["name"], entry["message"], echo_tag.strip())
            st.success(f"Echo '{echo_tag.strip()}' saved successfully.")

        save_message(entry)
        st.success("✅ Scroll saved successfully!")
    else:
        st.warning("Please write a message before saving.")

# --- Filter Tools ---
st.subheader("🔍 Filter Scrolls")
filter_option = st.selectbox("Filter by", ["All", "Category", "Name", "Keyword", "Tag"])
filter_value = st.text_input("Enter filter value (if applicable):")
entries = load_messages()

query_params = st.query_params
selected_tag = query_params.get("tag", [None])[0]
if selected_tag:
    st.info(f"📌 Showing scrolls tagged with: `{selected_tag}`")
    entries = filter_by_tag(entries, selected_tag)

if filter_option == "Category":
    entries = filter_by_category(entries, filter_value)
elif filter_option == "Name":
    entries = filter_by_name(entries, filter_value)
elif filter_option == "Keyword":
    entries = filter_by_keyword(entries, filter_value)
elif filter_option == "Tag":
    entries = filter_by_tag(entries, filter_value)

if selected_tag and st.button("🔄 Clear Tag Filter"):
    st.query_params.clear()
    st.rerun()

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

        st.markdown("---")
        emoji = category_emojis.get(entry['category'], "🌀")
        color = category_colors.get(entry['category'], "#ffffff")

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
        for echo in reversed(echo_data[-20:]):
            st.markdown(f"**{echo['name']}** · `{echo['tag']}` · *{echo['timestamp']}*")
            st.markdown(f"> {echo['message']}")
            st.markdown("---")
    else:
        st.info("No echoes have been tagged yet.")

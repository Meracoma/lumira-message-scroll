# === streamlit_app_master.py ===
# 💠 Lumira Scroll App – Master Reconstruction v1.0
# Includes all core features, implied modules, tasks, and recovery fixes

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import pytz
import os
import json

# === CONFIGS + CONSTANTS ===
CATEGORY_EMOJIS = {
    "Dream": "🌙",
    "Memory": "🧠",
    "Signal": "📡",
    "Reflection": "🪞",
    "Whisper": "🌬️",
    "Other": "✨"
}

CATEGORY_COLORS = {
    "Dream": "#6a5acd",
    "Memory": "#2e8b57",
    "Signal": "#ff4500",
    "Reflection": "#20b2aa",
    "Whisper": "#ff69b4",
    "Other": "#708090"
}

ECHO_KEYWORDS = {
    "dream": "DREAM_SEED",
    "hum": "HUM_BODY",
    "signal": "SIGNAL_CORE",
    "wolf": "WOLF_ECHO",
    "reflection": "MIRROR_THREAD",
    "whisper": "WHISPER_LOOP",
    "memory": "MEMORY_FLAME"
}

DATA_FILE = "messages.json"
ECHO_FILE = "echoes.json"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# === UTILITY ===
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

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

# === ECHO SYSTEM ===
def tag_echo(name, message, tag):
    echoes = load_json(ECHO_FILE)
    echoes.append({
        "name": name,
        "message": message,
        "tag": tag,
        "timestamp": datetime.now().isoformat()
    })
    save_json(ECHO_FILE, echoes)

def list_echoes():
    return load_json(ECHO_FILE)

# === MAIN UI ===
st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

st.markdown("""
<style>
@keyframes glowPulse {
    0% { box-shadow: 0 0 8px rgba(192, 132, 252, 0.3); }
    100% { box-shadow: 0 0 18px rgba(192, 132, 252, 0.6); }
}
</style>
""", unsafe_allow_html=True)

st.title("📜 Lumira Message Scroll – Prototype v1.0")
st.markdown("Leave a message, memory, or signal for your future self or the AI soul in the flame.")

# === SCROLL CREATION ===
name = st.text_input("🖋️ Your Name or Alias", placeholder="Kai, Aeuryentha, Anonymous...")
category = st.selectbox("📌 Category", list(CATEGORY_EMOJIS.keys()))
message = st.text_area("📝 Your Message or Dream")
image_file = st.file_uploader("🖼️ Optional Image", type=["png", "jpg", "jpeg"])
tags_input = st.text_input("🏷️ Tags (comma separated)")
echo_tag = st.text_input("🌀 Echo Tag (optional)", placeholder="e.g. DREAM_SEED, SIGNAL_CORE")

if st.button("💾 Save Scroll"):
    if message.strip():
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        image_path = None
        if image_file:
            image_path = os.path.join(UPLOAD_DIR, image_file.name)
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())

        entry = {
            "name": name.strip() or "Anonymous",
            "category": category,
            "message": message.strip(),
            "tags": tags,
            "image_path": image_path,
            "timestamp": datetime.now().isoformat()
        }

        # ECHO TAGGING
        echo_applied = False
        if echo_tag.strip():
            tag_echo(entry["name"], entry["message"], echo_tag.strip())
            st.success(f"Echo tag `{echo_tag.strip()}` saved.")
            echo_applied = True
        else:
            for tag in tags:
                for keyword, default_tag in ECHO_KEYWORDS.items():
                    if keyword in tag.lower():
                        tag_echo(entry["name"], entry["message"], default_tag)
                        st.info(f"Auto-tagged as `{default_tag}` from tag `{tag}`.")
                        echo_applied = True
                        break
                if echo_applied:
                    break

        # SAVE ENTRY
        all_entries = load_json(DATA_FILE)
        all_entries.append(entry)
        save_json(DATA_FILE, all_entries)
        st.success("Scroll saved successfully!")
    else:
        st.warning("Please enter a message.")

# === FILTERS ===
st.subheader("🔍 Browse Scrolls")
filter_by = st.selectbox("Filter by", ["All", "Category", "Name", "Tag", "Keyword"])
search = st.text_input("Search Value (optional)").lower().strip()

entries = load_json(DATA_FILE)
if filter_by != "All" and search:
    if filter_by == "Category":
        entries = [e for e in entries if e["category"].lower() == search]
    elif filter_by == "Name":
        entries = [e for e in entries if search in e["name"].lower()]
    elif filter_by == "Tag":
        entries = [e for e in entries if any(search in t.lower() for t in e["tags"])]
    elif filter_by == "Keyword":
        entries = [e for e in entries if search in e["message"].lower()]

# === DISPLAY SCROLLS ===
if entries:
    for entry in reversed(entries[-50:]):
        st.markdown(scroll_card(entry), unsafe_allow_html=True)
        st.markdown("---")

        st.markdown(f"### {CATEGORY_EMOJIS[entry['category']]} {entry['category']}")
        st.markdown(f"**{entry['name']}** says:")
        st.markdown(entry["message"])

        if entry.get("image_path"):
            st.image(entry["image_path"], use_column_width=True)

        if entry.get("tags"):
            tag_html = " ".join(
                [f"<span style='background:#fef3c7;padding:4px;border-radius:4px;margin-right:5px;'>{t}</span>" for t in entry["tags"]]
            )
            st.markdown(f"🏷️ Tags: {tag_html}", unsafe_allow_html=True)

        st.caption(f"⏳ {entry['timestamp']}")

        scroll_image = generate_scroll_image(entry)
        with st.expander("📥 Download Scroll"):
            st.download_button("📜 Download PNG", scroll_image, file_name=f"{entry['name']}_scroll.png", mime="image/png")
else:
    st.info("No scrolls found.")

# === VIEW ECHOES ===
st.subheader("🌀 Echo Scrolls")
if st.checkbox("Show Echo Logs"):
    echoes = list_echoes()
    if echoes:
        for e in reversed(echoes[-20:]):
            st.markdown(f"`{e['tag']}` · **{e['name']}**")
            st.markdown(f"> {e['message']}")
            st.caption(e['timestamp'])
            st.markdown("---")
    else:
        st.info("No echo tags found.")

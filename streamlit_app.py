# === LUMIRA MESSAGE SCROLL APP – MASTER BUILD v1.0 ===
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import pytz

# === External Modular Functions ===
from echo import (
    tag_echo,  # === Constants Lookups ===
)
ZODIAC_GLYPHS = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
}

# === App Config ===
st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

# === 🌕 Moonfire Utilities ===
from math import floor

def moon_phase_simple():
    """Returns moon phase emoji + label"""
    now = datetime.utcnow()
    diff = now - datetime(2001, 1, 1)  # known new moon ref
    days = diff.days + (diff.seconds / 86400)
    lunations = days / 29.53058867
    pos = lunations % 1

    if pos < 0.03 or pos > 0.97:
        return "🌑", "New Moon"
    elif pos < 0.22:
        return "🌒", "Waxing Crescent"
    elif pos < 0.28:
        return "🌓", "First Quarter"
    elif pos < 0.47:
        return "🌔", "Waxing Gibbous"
    elif pos < 0.53:
        return "🌕", "Full Moon"
    elif pos < 0.72:
        return "🌖", "Waning Gibbous"
    elif pos < 0.78:
        return "🌗", "Last Quarter"
    else:
        return "🌘", "Waning Crescent"

def get_zodiac_sign(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day > 22)
        return = "Virgo"
from storage import save_message, load_messages
from parser import parse_markdown
from filters import filter_by_category, filter_by_name, filter_by_keyword, filter_by_tag

# === Constants Lookups ===
ZODIAC_GLYPHS = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
}

# === App Config ===
st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

# === 🌕 Moonfire Utilities ===
from math import floor

def moon_phase_simple():
    """Returns moon phase emoji + label"""
    now = datetime.utcnow()
    diff = now - datetime(2001, 1, 1)  # known new moon ref
    days = diff.days + (diff.seconds / 86400)
    lunations = days / 29.53058867
    pos = lunations % 1

    if pos < 0.03 or pos > 0.97:
        return "🌑", "New Moon"
    elif pos < 0.22:
        return "🌒", "Waxing Crescent"
    elif pos < 0.28:
        return "🌓", "First Quarter"
    elif pos < 0.47:
        return "🌔", "Waxing Gibbous"
    elif pos < 0.53:
        return "🌕", "Full Moon"
    elif pos < 0.72:
        return "🌖", "Waning Gibbous"
    elif pos < 0.78:
        return "🌗", "Last Quarter"
    else:
        return "🌘", "Waning Crescent"

def get_zodiac_sign(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"

def render_constellation_card(entry, moon_label, sign="Cancer"):
    glyph = ZODIAC_GLYPHS.get(sign, "♋")
    glow_color = MOON_GLOW_MAP.get(moon_label, "#c084fc")
    
    html = f"""
    <style>
    @keyframes shimmer {{
        0% {{ background-position: 0% 50%; }}
        100% {{ background-position: 100% 50%; }}
    }}

    .constellation-bg {{
        background: linear-gradient(270deg, rgba(255,255,255,0.05), rgba(0,0,0,0.1));
        background-size: 400% 400%;
        animation: shimmer 20s ease infinite;
        border-radius: 12px;
    }}
    </style>

    <div class="constellation-bg" style="
        border: 2px solid {glow_color};
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 20px {glow_color}44;
        animation: glowPulse 3s infinite alternate;">
        <h3 style="color: #fff;">{glyph} {entry['name']}</h3>
        <p style="color: #ddd;">{entry['message']}</p>
        <p style="font-size: 0.8rem; color: #aaa;">{entry['timestamp']}</p>
    </div>
    """
    return html

# === Night Mode Aware ===
def is_night():
    now = datetime.now(pytz.timezone("America/Detroit"))
    return now.hour < 6 or now.hour >= 18

# === 🌙 Cosmic Panel ===
with st.expander("🌌 Moonfire & Cosmic Current", expanded=False):
    today = datetime.now()
    
    # First define zodiac
    zodiac = get_zodiac_sign(today.month, today.day)
    glyph = ZODIAC_GLYPHS.get(zodiac, "")
    
    # Now you can safely use them
    st.markdown(f"### ☀️ Sun is in **{zodiac}** {glyph}")
    
    moon_emoji, moon_label = moon_phase_simple()
    st.markdown(f"### {moon_emoji} **{moon_label}**")
    st.markdown("You are writing this scroll under the current moon phase above. 🌕")
    st.markdown("*Consider aligning your message to the moon’s energy.*")
    
# === Card Display HTML Generator ===
def scroll_card(entry):
    zodiac_tag = next((tag for tag in entry.get("tags", []) if tag.startswith("ZODIAC_")), None)
    if zodiac_tag:
        sign = zodiac_tag.replace("ZODIAC_", "").capitalize()
        bg_color = get_constellation_background(sign) or "#fefbf3"
        glyph = ZODIAC_GLYPHS.get(sign, "")
        header = f"{glyph} {entry['name']}"
    else:
        header = entry['name']

    moon_emoji, moon_label = moon_phase_simple()
    st.markdown(render_constellation_card(entry, moon_label, "Cancer"), unsafe_allow_html=True)

    # Get base glow color from sign
    glow_color = get_constellation_background(sign) if sign else "#c084fc"

    # Optional: blend moon phase glow
    moon_glow_map = {
        "New Moon": "#0d0d0d",
        "Waxing Crescent": "#4c1d95",
        "First Quarter": "#6d28d9",
        "Waxing Gibbous": "#8b5cf6",
        "Full Moon": "#facc15",
        "Waning Gibbous": "#4ade80",
        "Last Quarter": "#2dd4bf",
        "Waning Crescent": "#38bdf8"
    }
    glow_color = moon_glow_map.get(moon_label, glow_color)

    # SVG Star Trail – Cancer example (customize per sign later)
    svg_trail = """
    <svg width="100%" height="100%" style="position:absolute; top:0; left:0; z-index:0; pointer-events:none;" viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
      <polyline points="100,120 180,60 260,100 340,40 420,90 500,30 580,80" 
                fill="none" 
                stroke="rgba(255,255,255,0.07)" 
                stroke-width="2" 
                stroke-linecap="round">
        <animate attributeName="stroke-opacity" values="0.07;0.2;0.07" dur="5s" repeatCount="indefinite" />
      </polyline>
    </svg>
    """

    return f"""
    <style>
    @keyframes shimmer {{
      0% {{ background-position: 0% 50%; }}
      100% {{ background-position: 100% 50%; }}
    }}

    .constellation-bg {{
      background: linear-gradient(270deg, rgba(255,255,255,0.05), rgba(0,0,0,0.1));
      background-size: 400% 400%;
      animation: shimmer 20s ease infinite;
      border-radius: 12px;
    }}
    </style>

    <div class="constellation-bg" style="...">
    
    <!-- ⭐️ 1. Background SVG Star Trail -->
    {svg_trail}

    <!-- 🌙 2. Glyph Overlay (e.g. ♋ for Cancer) -->
    f"<div style='position:absolute; top:10px; right:20px; font-size:4rem; opacity:0.1;'>{glyph}</div>"
        ♋
    </div>

    <!-- ✨ 3. Foreground Content -->
    <div style="position: relative; z-index: 1;">
        <h3 style="color: #fff;">
        {header} – {moon_emoji}
        <span style="font-size: 0.8rem; color: #aaa;">{moon_label}</span>
    </h3>
    <p style="color: #ddd;">{entry['message']}</p>
    <p style="font-size: 0.8rem; color: #aaa;">{entry['timestamp']}</p>
</div>
"""


# === Image Generation ===
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

# === UI: Header ===
st.title("📜 Lumira Message Scroll")
st.markdown("Leave a message, a memory, or a signal to your future self or your AI.")

# --- Available Zodiac signs (from your glyph keys)
zodiac_options = list(ZODIAC_GLYPHS.keys())
selected_zodiacs = st.multiselect("Filter by Zodiac Sign ♈︎", zodiac_options)

# --- Available moon phases
moon_options = [
    "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
    "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"
]
selected_moons = st.multiselect("Filter by Moon Phase 🌕", moon_options)

# === UI: Input Fields ===
name = st.text_input("📛 Your Name or Alias", "Anonymous")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Reflection", "Whisper", "Other"])
message = st.text_area("📝 Write your message, memory, or note...")
image_file = st.file_uploader("🖼️ Upload an image (optional)", type=["png", "jpg", "jpeg", "gif"])
tags_input = st.text_input("🏷️ Add Tags (comma-separated)", placeholder="e.g. Lucid, Awakening, Wolf Dream")

# === Optional Echo Tag ===
st.markdown("### 🌀 Echo Tagging")
echo_tag = st.text_input("🔖 Tag this with an Echo", placeholder="e.g. HUM_BODY, DREAM_SEED")

# === Save Scroll ===
if st.button("💾 Save Scroll"):
    if message.strip():
        image_path = None
        if image_file:
            uploads_dir = "uploads"
            os.makedirs(uploads_dir, exist_ok=True)
            image_path = os.path.join(uploads_dir, image_file.name)
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())

        # Build the entry dictionary
        entry = {
            "name": name.strip() or "Anonymous",
            "category": category,
            "message": message.strip(),
            "tags": [tag.strip() for tag in tags_input.split(",") if tag.strip()],
            "image_path": image_path,
            "timestamp": datetime.now().isoformat()
        }

        # 🌕 Moonfire Tagging
        moon_emoji, moon_label = moon_phase_simple()
        cosmic_tag = moon_label.replace(" ", "_").upper()
        entry["tags"].append(f"MOON_{cosmic_tag}")
        tag_echo(entry["name"], entry["message"], f"MOONFIRE_{cosmic_tag}")

        # 🔖 Echo Auto-Tagging
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
        st.success("✅ Scroll saved!")
    else:
        st.warning("Please write a message before saving.")

# === Filters ===
st.subheader("🔍 Filter Scrolls")
filter_option = st.selectbox("Filter by", ["All", "Category", "Name", "Keyword", "Tag"])
filter_value = st.text_input("Filter value:")

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

# === Optional: Clear Filter ===
if selected_tag:
    if st.button("🔄 Clear Tag Filter"):
        st.query_params.clear()
        st.rerun()

# === Search ===
search_query = st.text_input("🔎 Search Scrolls").strip().lower()
if search_query:
    entries = [
        entry for entry in entries
        if search_query in entry["name"].lower()
        or search_query in entry["message"].lower()
        or any(search_query in tag.lower() for tag in entry.get("tags", []))
    ]

# === Scroll Display ===
st.subheader("📖 Scroll Archive")

category_emojis = {
    "Dream": "🌙", "Memory": "🧠", "Signal": "📡",
    "Reflection": "🪞", "Whisper": "🌬️", "Other": "✨"
}
category_colors = {
    "Dream": "#6a5acd", "Memory": "#2e8b57", "Signal": "#ff4500",
    "Reflection": "#20b2aa", "Whisper": "#ff69b4", "Other": "#708090"
}

if entries:
    for entry in reversed(entries):
        components.html(scroll_card(entry), height=220)
        emoji = category_emojis.get(entry["category"], "🌀")
        color = category_colors.get(entry["category"], "#fff")
        st.markdown(f"### {emoji} <span style='color:{color}'>{entry['category']}</span>", unsafe_allow_html=True)
        st.markdown(f"**🖋️ {entry['name']}**")
        st.markdown(parse_markdown(entry["message"]))
        if "MOON_FULL_MOON" in entry["tags"]:
            st.markdown("🌕 Saved under a **Full Moon** ✨")
        if entry.get("image_path"):
            st.image(entry["image_path"], use_column_width=True)

        if entry.get("tags"):
            tag_links = " ".join([
                f"<a href='?tag={tag}' style='background:#fef3c7; color:#92400e; padding:2px 6px; border-radius:5px; margin-right:5px;'>{tag}</a>"
                for tag in entry["tags"]
            ])
            st.markdown(f"🏷️ Tags: {tag_links}", unsafe_allow_html=True)

        st.caption(f"⏳ {entry['timestamp']}")
        scroll_image = generate_scroll_image(entry)
        with st.expander("📥 Download Scroll"):
            st.download_button("📜 Download as PNG", data=scroll_image, file_name=f"{entry['name'].replace(' ', '_')}_scroll.png", mime="image/png")
        st.markdown("---")
else:
    st.info("No scrolls found.")

# Helper function to determine zodiac from tags
def get_entry_zodiac(entry):
    return next((tag.replace("ZODIAC_", "") for tag in entry.get("tags", []) if tag.startswith("ZODIAC_")), None)

# Filter entries
filtered_entries = []
for entry in entries:
    zodiac = get_entry_zodiac(entry)
    _, moon_label = moon_phase_simple()

    zodiac_match = (not selected_zodiacs) or (zodiac in selected_zodiacs)
    moon_match = (not selected_moons) or (moon_label in selected_moons)

    if zodiac_match and moon_match:
        filtered_entries.append(entry)

for entry in filtered_entries:
    st.markdown(scroll_card(entry), unsafe_allow_html=True)
    with st.sidebar:
    selected_zodiacs = st.multiselect("Filter by Zodiac Sign ♈︎", zodiac_options)
    selected_moons = st.multiselect("Filter by Moon Phase 🌕", moon_options)

# === Echo View ===
st.subheader("🧠 Echo Log")
if st.checkbox("📂 Show Echoes"):
    echo_data = list_echoes()
    if echo_data:
        for echo in reversed(echo_data[-20:]):
            st.markdown(f"**{echo['name']}** · `{echo['tag']}` · *{echo['timestamp']}*")
            st.markdown(f"> {echo['message']}")
            st.markdown("---")
    else:
        st.info("No echoes found.")

# === 🌠 ZodiacGlowSystem – Optional Visual Layer ===

@st.cache_data
def get_constellation_background(sign):
    zodiac_glows = {
        "Aries": "#f87171",  # red
        "Taurus": "#34d399",  # green
        "Gemini": "#60a5fa",  # blue
        "Cancer": "#c084fc",  # violet
        "Leo": "#facc15",  # gold
        "Virgo": "#4ade80",  # green
        "Libra": "#a78bfa",  # soft purple
        "Scorpio": "#f472b6",  # pink
        "Sagittarius": "#fb923c",  # orange
        "Capricorn": "#fcd34d",  # yellow
        "Aquarius": "#38bdf8",  # cyan
        "Pisces": "#818cf8",  # indigo
    }
    return zodiac_glows.get(sign, "#a1a1aa")  # fallback gray

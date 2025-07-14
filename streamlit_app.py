# === 📜 LUMIRA SCROLL APP – CORE SETUP ===

# 🧩 External Libraries
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import pytz

# 🧠 Local Modules (modular helpers)
from storage import save_message, load_messages
from parser import parse_markdown
from filters import (
    filter_by_category,
    filter_by_name,
    filter_by_keyword,
    filter_by_tag
)

# 🌌 Echo System Integration
from echo import tag_echo  # Optional echo tagging system

# 🌍 Timezone Setting
TZ = pytz.timezone("America/Detroit")

# 🪄 Streamlit App Layout Config
st.set_page_config(
    page_title="📜 Lumira Message Scroll",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🗂️ Session State Memory Init (favorites + echo logs)
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "echo_log" not in st.session_state:
    st.session_state.echo_log = []

if "active_tag" not in st.session_state:
    st.session_state.active_tag = None

# === 🌙 MOON PHASE + SUN ZODIAC SYSTEM ===

from math import floor
from datetime import datetime as dt

# === 🌈 MOON GLOW AESTHETIC MAPPING ===

MOON_GLOW_MAP = {
    "New Moon":         "#111827",  # Deep black/blue (mystery, seed)
    "Waxing Crescent":  "#6d28d9",  # Indigo / purple (potential, memory forming)
    "First Quarter":    "#4f46e5",  # Royal blue (courage, rise)
    "Waxing Gibbous":   "#7c3aed",  # Violet (anticipation, gestation)
    "Full Moon":        "#facc15",  # Radiant gold (revelation, climax)
    "Waning Gibbous":   "#f59e0b",  # Amber (reflection, gratitude)
    "Last Quarter":     "#e11d48",  # Rose red (release, letting go)
    "Waning Crescent":  "#6b7280",  # Ash grey (compost, return to source)
}

# 🌘 Moon Phase Detection (Simple)
def moon_phase_simple():
    """
    Returns current moon phase emoji + label
    using a known new moon baseline from Jan 1, 2001.
    """
    now = dt.utcnow()
    diff = now - dt(2001, 1, 1)  # Reference new moon date
    days = diff.days + (diff.seconds / 86400)
    lunations = days / 29.53058867  # Length of lunar cycle
    pos = lunations % 1  # Fractional position in cycle

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

# ☀️ Sun Zodiac Sign by Date
def get_zodiac_sign(month, day):
    """
    Returns Western Zodiac sign from calendar month/day.
    Used for solar-based Zodiac lookup.
    """
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
    else:
        return None  # Fallback for invalid dates

# === ♓ ZODIAC SIGN & GLYPH LOOKUP ===

# ♈ Zodiac Sign Determination (based on Gregorian date)
def get_zodiac_sign(month: int, day: int) -> str:
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
    return "Unknown"

# ♑ Zodiac Glyphs for each sign
ZODIAC_GLYPHS = {
    "Aries": "♈",      "Taurus": "♉",     "Gemini": "♊",     "Cancer": "♋",
    "Leo": "♌",        "Virgo": "♍",      "Libra": "♎",      "Scorpio": "♏",
    "Sagittarius": "♐","Capricorn": "♑", "Aquarius": "♒",   "Pisces": "♓"
}

# 🜁 Optional: Element Mapping for elemental integration (future add-ons)
ZODIAC_ELEMENTS = {
    "Aries": "Fire",     "Leo": "Fire",       "Sagittarius": "Fire",
    "Taurus": "Earth",   "Virgo": "Earth",    "Capricorn": "Earth",
    "Gemini": "Air",     "Libra": "Air",      "Aquarius": "Air",
    "Cancer": "Water",   "Scorpio": "Water",  "Pisces": "Water"
}

# === ⭐ FAVORITES & 📣 ECHO LOG SESSION STATE ===

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "echo_log" not in st.session_state:
    st.session_state.echo_log = []

# Optional: Unified toggle access helper (if needed later)
def is_favorited(entry_timestamp: str) -> bool:
    return entry_timestamp in st.session_state.favorites

def toggle_favorite(entry_timestamp: str):
    if entry_timestamp in st.session_state.favorites:
        st.session_state.favorites.remove(entry_timestamp)
    else:
        st.session_state.favorites.append(entry_timestamp)

def log_to_echo(entry):
    st.session_state.echo_log.append(entry)

# === 🌌 SCROLL CARD RENDER FUNCTION ===

def render_scroll_card(entry, moon_label, zodiac_sign):
    glyph = ZODIAC_GLYPHS.get(zodiac_sign, "♋")
    glow_color = MOON_GLOW_MAP.get(moon_label, "#c084fc")  # Default: violet
    name_display = entry['name']
    timestamp = entry.get("timestamp", "⏳ Unknown Time")
    tags = entry.get("tags", [])

    # Check if marked as favorite
    is_fav = entry.get("favorite", False) or (timestamp in st.session_state.favorites)
    if is_fav:
        name_display = f"⭐ {name_display}"

    # Render tags as interactive pill links
    tag_html = ""
    if tags:
        tag_html = "🏷️ "
        for tag in tags:
            tag_html += f"""
                <a href='?tag={tag}' onclick="window.location.reload()" style='
                    background:#fef3c7;
                    color:#92400e;
                    padding:2px 6px;
                    border-radius:6px;
                    margin-right:6px;
                    text-decoration:none;
                    font-weight:bold;
                    font-size: 0.75rem;'>{tag}</a>
            """

    html = f"""
    <style>
    @keyframes shimmer {{
        0% {{ background-position: 0% 50%; }}
        100% {{ background-position: 100% 50%; }}
    }}
    .constellation-bg {{
        background: linear-gradient(270deg, rgba(255,255,255,0.05), rgba(0,0,0,0.15));
        background-size: 400% 400%;
        animation: shimmer 20s ease infinite;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.2rem;
        border: 2px solid {glow_color};
        box-shadow: 0 0 20px {glow_color}55;
    }}
    </style>

    <div class="constellation-bg">
        <h3 style="color: #fff;">{glyph} {name_display}</h3>
        <p style="color: #ddd;">{entry['message']}</p>
        <p style="font-size: 0.8rem; color: #aaa;">{timestamp}</p>
        <div style="margin-top: 0.5rem;">{tag_html}</div>
    </div>
    """

    st.components.v1.html(html, height=260)

    # Echo + Favorite Control Row
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📣 Send to Echo Log", key=f"echo_{timestamp}"):
            log_to_echo(entry)
            tag_echo(entry["name"], entry["message"], "SCROLL_PING")
            st.success("📡 Scroll echoed to memory log!")

    with col2:
        current_fav_state = timestamp in st.session_state.favorites
        if st.checkbox("⭐ Mark as Favorite", value=current_fav_state, key=f"fav_{timestamp}"):
            if not current_fav_state:
                st.session_state.favorites.append(timestamp)
        else:
            if current_fav_state:
                st.session_state.favorites.remove(timestamp)

# === 🔎 FILTER HANDLERS — FINAL + PHASE 3 READY ===

def apply_filters(messages, name=None, keyword=None, category=None, tag=None):
    """
    Apply all selected filters to the message list.
    Each filter is optional and layered sequentially.
    Enhanced with case-insensitive matching, tag rerun, and echo logging.
    """
    filtered = messages

    # Normalize inputs to lowercase for case-insensitive matching
    if name:
        name = name.lower()
    if keyword:
        keyword = keyword.lower()
    if category:
        category = category.lower()
    if tag:
        tag = tag.lower()

    # 🌿 Echo log message
    filter_debug_msg = f"[🌀 FILTER APPLIED] → Name: {name}, Keyword: {keyword}, Category: {category}, Tag: {tag}"
    print(filter_debug_msg)

    # 🌊 Echo memory stream (Phase 3 forward-compatible)
    if "echo_log" in st.session_state:
        st.session_state.echo_log.append({
            "type": "filter",
            "timestamp": datetime.now().isoformat(),
            "details": {
                "name": name,
                "keyword": keyword,
                "category": category,
                "tag": tag
            },
            "note": filter_debug_msg
        })

    # Apply filters
    if name:
        filtered = [m for m in filtered if name in m.get('name', '').lower()]

    if keyword:
        filtered = [m for m in filtered if keyword in m.get('message', '').lower()]

    if category:
        filtered = [m for m in filtered if category in m.get('category', '').lower()]

    if tag:
        filtered = [m for m in filtered if tag in [t.lower() for t in m.get('tags', [])]]
        # Enhance UX: rerun with tag param
        st.experimental_set_query_params(tag=tag)

    return filtered

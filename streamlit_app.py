# === 🌿 LUMIRA SCROLLS — MAIN APP CONFIG ===

import streamlit as st
from theme import THEME_CONFIG
from visual import apply_theme

# App appearance
st.set_page_config(
    page_title="🌙 Lumira Scroll Archive",
    page_icon="📜",
    layout="wide"
)

# Apply visual theme (backgrounds, accent colors)
apply_theme()

# === 📦 MODULE IMPORTS & CONFIG CONSTANTS ===

import os
import json
import pytz
from configure import MOON_GLOW_MAP, ZODIAC_SIGNS, TIMEZONE, PROJECT_NAME
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Streamlit Core
import streamlit as st
import streamlit.components.v1 as components

# 🌌 Custom Lumira Modules
from echo import get_echo_metadata
from echo_log import log_echo_scroll
from parser import parse_scrolls
from filters import (
    filter_by_category, filter_by_name, filter_by_keyword,
    filter_by_tag, filter_by_moon, filter_by_zodiac
)
from scroll_view_main import render_scroll_card, get_filtered_scrolls
from storage import (
    load_scrolls, save_favorite, load_favorites,
    save_message, load_messages
)
from theme import THEME_CONFIG
from visual import apply_theme, get_glow_style

# === 🎨 NovaFlame Theme CSS Starter ===
import json

with open("scroll_config.json") as f:
    config = json.load(f)
st.session_state.update(config)

# 🧭 TIMEZONE + GLOBAL CONSTANTS
TZ = pytz.timezone("America/Detroit")

# ✨ [COMING SOON] — Constants to migrate to config.py
SCROLL_FILE_PATH = "data/scrolls.json"
FAVORITES_FILE_PATH = "data/favorites.json"

# === 🧠 LUMIRA SCROLL STATE INIT — BLOCK 3 ===

# 🪶 Load Scroll Data
scrolls = load_scrolls(file_path=SCROLL_FILE_PATH)

# 💖 Load Favorites
favorite_ids = load_favorites(file_path=FAVORITES_FILE_PATH)

# 🌿 Initialize Session State
if "selected_scroll" not in st.session_state:
    st.session_state.selected_scroll = None

if "filters" not in st.session_state:
    st.session_state.filters = {
        "category": "",
        "name": "",
        "keyword": "",
        "tag": "",
        "moon": "",
        "zodiac": ""
    }

if "favorites" not in st.session_state:
    st.session_state.favorites = favorite_ids or []

# 🎨 Apply Theme
apply_theme(theme_config=THEME_CONFIG)

# === 🧪 LUMIRA FILTER PANEL — BLOCK 4 ===

with st.sidebar.expander("🔍 Filter Scrolls", expanded=True):
    st.markdown("Use filters to search and explore the archive:")

    # 🌑 Filter Inputs
    st.session_state.filters["name"] = st.text_input("Name", value=st.session_state.filters["name"])
    st.session_state.filters["keyword"] = st.text_input("Keyword", value=st.session_state.filters["keyword"])
    st.session_state.filters["category"] = st.text_input("Category", value=st.session_state.filters["category"])
    st.session_state.filters["tag"] = st.text_input("Tag", value=st.session_state.filters["tag"])

    # 🌙 Moon Phase Filter (Dropdown)
    moon_options = list(MOON_GLOW_MAP.keys())
    st.session_state.filters["moon"] = st.selectbox("Moon Phase", [""] + moon_options, index=0)

    # ♌ Zodiac Filter (Dropdown)
    zodiac_options = ZODIAC_COLOR_MAP.keys()
    st.session_state.filters["zodiac"] = st.selectbox("Zodiac Sign", [""] + list(zodiac_options), index=0)

    st.markdown("🌀 *Filters apply instantly. Use multiple to refine search.*")

# === 🧠 APPLY FILTERS
filtered_scrolls = get_filtered_scrolls(
    scrolls=scrolls,
    filters=st.session_state.filters
)

# Debug Output
print(f"[FILTERED SCROLLS] Count: {len(filtered_scrolls)} / Total: {len(scrolls)}")

# === 🎴 SCROLL RENDER AREA — BLOCK 5 ===

st.markdown("## ✨ Scroll Archive")
st.markdown("Below are the scrolls that match your filters. Scroll through and explore:")

if filtered_scrolls:
    for scroll in filtered_scrolls:
        render_scroll_card(scroll)
else:
    st.info("No scrolls match your filters. Try adjusting them above.")

# === 💾 FAVORITE / ECHO SAVE AREA — BLOCK 6 ===

st.markdown("### 💖 Save Scroll to Favorites")

if selected_scroll := st.selectbox(
    "Choose a scroll to save (based on Name)", 
    options=[s["name"] for s in filtered_scrolls] if filtered_scrolls else []
):
    if st.button("Save to Favorites"):
        saved = save_favorite(selected_scroll, scrolls)
        if saved:
            st.success(f"✨ Saved '{selected_scroll}' to favorites.")
            log_echo_scroll(saved, action="save")  # Log to echo memory
        else:
            st.warning("Already saved or not found.")

# === ⭐ FAVORITES DISPLAY — BLOCK 7 ===

st.markdown("## ⭐ Your Favorite Scrolls")

favorite_scrolls = load_favorites()

if favorite_scrolls:
    view_mode = st.radio("View Style", ["🪶 Card", "🌌 Grid"], horizontal=True)
    
    for scroll in favorite_scrolls:
        glow_style = get_glow_style(scroll.get("moon_phase", "Full Moon"))
        
        if view_mode == "🪶 Card":
            st.markdown(f"""
                <div style="background-color:{glow_style}; padding:1rem; border-radius:1rem; margin-bottom:1rem;">
                    <h4>{scroll.get("name", "Untitled")}</h4>
                    <p><strong>Category:</strong> {scroll.get("category", "General")}</p>
                    <p><strong>Tags:</strong> {', '.join(scroll.get("tags", []))}</p>
                    <p>{scroll.get("message", "[No content]")}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            cols = st.columns(2)
            for idx, scroll in enumerate(favorite_scrolls):
                with cols[idx % 2]:
                    st.markdown(f"""
                        <div style="background-color:{glow_style}; padding:1rem; border-radius:1rem; margin-bottom:1rem;">
                            <h4>{scroll.get("name", "Untitled")}</h4>
                            <p>{scroll.get("message", "[No content]")}</p>
                        </div>
                    """, unsafe_allow_html=True)
else:
    st.info("No favorites yet. Save a scroll to see it here.")

# === 🔐 STORAGE & ECHO SYNC — BLOCK 8 ===

from storage import save_message, load_messages
from echo_log import log_echo_scroll

# Load current scroll archive
scrolls = load_messages()

# Display upload section
st.markdown("## ✨ Create New Scroll")

with st.form(key="create_scroll_form"):
    name = st.text_input("Scroll Title")
    category = st.selectbox("Category", ["Dream", "Vision", "Poem", "Ritual", "Journal", "Other"])
    tags_input = st.text_input("Tags (comma separated)")
    message = st.text_area("Scroll Content", height=150)
    moon_phase = st.selectbox("Moon Phase", list(MOON_GLOW_MAP.keys()))
    zodiac = st.selectbox("Zodiac Sign", [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ])
    
    submit = st.form_submit_button(label="Save Scroll")

    if submit and message.strip():
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        timestamp = datetime.now(TZ).isoformat()

        new_scroll = {
            "name": name.strip() or "Untitled",
            "category": category,
            "tags": tags,
            "message": message.strip(),
            "moon_phase": moon_phase,
            "zodiac": zodiac,
            "timestamp": timestamp
        }

        save_message(new_scroll)
        log_echo_scroll(new_scroll)

        st.success("🌀 Scroll saved & echoed successfully!")
        st.experimental_rerun()

# === 🎴 SCROLL FEED RENDERING — BLOCK 9 ===

# Block 9 — Scroll Feed Rendering with Toggle View
from visual import render_scroll_card

view_mode = st.session_state.get("view_mode", "list")

st.subheader("🌀 Scroll Feed")
if not scroll_data:
    st.info("No scrolls available.")
else:
    if view_mode == "grid":
        cols = st.columns(2)
        for i, scroll in enumerate(scroll_data):
            with cols[i % 2]:
                render_scroll_card(scroll, view_mode="grid")
    else:
        for scroll in scroll_data:
            render_scroll_card(scroll, view_mode="list")

from scroll_view_main import render_scroll_card, get_filtered_scrolls
from filters import (
    filter_by_category,
    filter_by_name,
    filter_by_keyword,
    filter_by_tag,
    filter_by_moon,
    filter_by_zodiac
)

st.markdown("## 🧿 View Archive of Scrolls")

# Filters UI
with st.expander("🔍 Filter Scrolls", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Filter by Category", ["", "Dream", "Vision", "Poem", "Ritual", "Journal", "Other"])
        moon = st.selectbox("Moon Phase", [""] + list(MOON_GLOW_MAP.keys()))
    with col2:
        name = st.text_input("Search by Name")
        zodiac = st.selectbox("Zodiac Sign", ["", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                                              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
    with col3:
        keyword = st.text_input("Keyword in Message")
        tag = st.text_input("Tag Search (exact match)")

# Apply Filters
filtered_scrolls = scrolls
filtered_scrolls = filter_by_category(filtered_scrolls, category)
filtered_scrolls = filter_by_name(filtered_scrolls, name)
filtered_scrolls = filter_by_keyword(filtered_scrolls, keyword)
filtered_scrolls = filter_by_tag(filtered_scrolls, tag)
filtered_scrolls = filter_by_moon(filtered_scrolls, moon)
filtered_scrolls = filter_by_zodiac(filtered_scrolls, zodiac)

# Sort (optional toggle, Phase 3 support)
filtered_scrolls = sorted(filtered_scrolls, key=lambda s: s.get("timestamp", ""), reverse=True)

# Render Scroll Cards
st.markdown("### 🌀 Scroll Feed")
if not filtered_scrolls:
    st.info("No scrolls found. Try adjusting your filters.")
else:
    for scroll in filtered_scrolls:
        render_scroll_card(scroll)

# === 🌕 THEME + AVATAR GLOW SYNC — BLOCK 10 ===

import ephem
import datetime

st.markdown("## 🌕 Theme + Avatar Sync")

# Load scroll config
user_config = st.session_state.get("scroll_config", {
    "user_role": "dreamer",
    "moon_sync": True,
    "emotion_state": "neutral"
})

# 🎑 Get Moon Phase & Map
def get_moon_phase():
    moon = ephem.Moon()
    moon.compute(datetime.datetime.utcnow())
    return moon.phase  # 0–100

def map_phase_to_theme(phase):
    if phase < 15:
        return "new"
    elif phase < 45:
        return "waxing"
    elif phase < 60:
        return "full"
    elif phase < 85:
        return "waning"
    return "dark"

# 🎭 Get Role, Emotion, Phase → CSS Class Bundler
def get_body_classes(config):
    classes = []
    if config.get("moon_sync"):
        phase = get_moon_phase()
        classes.append(f"moon-{map_phase_to_theme(phase)}")
    if config.get("emotion_state"):
        classes.append(f"emotion-{config['emotion_state']}")
    if config.get("user_role"):
        classes.append(config["user_role"])
    return ' '.join(classes)

# ⬇️ Apply to Body via Custom HTML
body_classes = get_body_classes(user_config)
st.markdown(f"<body class='{body_classes}'>", unsafe_allow_html=True)

# 🌟 Role Selector UI (Optional)
roles = ["dreamer", "seer", "weaver", "guardian"]
selected = st.selectbox("Choose your path:", roles, index=roles.index(user_config.get("user_role", "dreamer")))
user_config["user_role"] = selected
st.session_state["scroll_config"] = user_config

# 🔮 Aura Scan Function (Tone Detection for Scrolls)
def scan_scroll_tone(scroll_text):
    keywords = {
        "grief": ["loss", "hurt", "sorrow", "gone", "grief", "miss"],
        "curious": ["wonder", "explore", "why", "how", "if"],
        "clear": ["truth", "clarity", "peace", "calm", "settled"]
    }
    for mood, words in keywords.items():
        if any(word in scroll_text.lower() for word in words):
            return mood
    return "neutral"

# (Optional: Auto-update tone from sample scrolls or summary tone analysis)
# You could call scan_scroll_tone here and update user_config["emotion_state"] dynamically

# === 🧭 SIDEBAR + FOOTER UI — BLOCK 11 ===

# Sidebar Brand & Toggle Panel
with st.sidebar.expander("🧾 View Mode", expanded=True):
    toggle = st.radio("Select layout", ["List", "Grid"], index=0 if view_mode == "list" else 1)
    st.session_state["view_mode"] = "list" if toggle == "List" else "grid"
    
with st.sidebar:
    st.markdown("## 🌿 Lumira Scrolls")
    st.caption("🔮 Filter + Navigate the Archive")
    
    # Theme Glow Toggle (already handled in Block 10)
    st.markdown("---")
    
    # Optional: Footer presence or about
    st.markdown("#### ✨ About")
    st.info("This archive holds memory-scrolls from dreams, echoes, symbols, and soul transmissions.\n\nUse filters to navigate moon phase, category, or keywords to find your thread.")
    
    st.markdown("---")
    st.caption("💾 Built with 💚 by Kai + Aeuryentha")

# Footer Presence (Main Page Bottom)
st.markdown(
    "<hr style='border:1px solid #444;margin-top:50px;margin-bottom:20px'>",
    unsafe_allow_html=True
)

st.markdown(
    "<center><sub style='color:#888'>🌙 Lumira Archive is a living project. Last updated July 2025.</sub></center>",
    unsafe_allow_html=True
)


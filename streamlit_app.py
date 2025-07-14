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
from datetime import datetime
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


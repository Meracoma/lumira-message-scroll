# === 🌿 LUMIRA SCROLL ARCHIVE MAIN APP — streamlit_app.py ===

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json
import os
import pytz

# === 🧠 LOCAL MODULE IMPORTS ===

# Core Filters
from filters import (
    filter_by_category, filter_by_name, filter_by_keyword,
    filter_by_tag, filter_by_moon, filter_by_zodiac
)

# Scroll System
from parser import parse_scrolls, parse_markdown
from scroll_view_main import render_scroll_card, get_filtered_scrolls
from storage import load_scrolls, save_message, load_messages, save_favorite, load_favorites

# Echo + Visual
from echo import get_echo_metadata, tag_echo
from echo_log import log_echo_scroll
from visual import apply_theme, get_glow_style
from theme import THEME_CONFIG

# === 🌎 TIMEZONE CONFIG ===
TZ = pytz.timezone("America/Detroit")

# === 🛠️ STREAMLIT CONFIG ===
st.set_page_config(page_title="Lumira Scrolls", layout="wide")

# === 🎛️ LUMIRA FILTER PANEL (Sidebar UI) ===

with st.sidebar:
    st.markdown("## 🔮 Filter Scrolls")

    # 🌕 Moon Phase Filter
    selected_moon = st.selectbox(
        "🌙 Moon Phase",
        options=["", "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
                 "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"],
        index=0,
        help="Filter scrolls based on lunar energy."
    )

    # ♒ Zodiac Sign Filter
    selected_zodiac = st.selectbox(
        "♒ Zodiac Sign",
        options=["", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"],
        index=0,
        help="Filter scrolls tied to zodiac archetypes."
    )

    # 🗓️ Date Filter Toggle
    sort_by_date = st.checkbox("📅 Sort by Date (Newest First)", value=False)
    show_today_only = st.checkbox("📆 Only Show Today’s Scrolls", value=False)

    # 🔖 Echo Tag Input
    echo_tag = st.text_input("🌀 Tag this with an Echo", placeholder="e.g. HUM_BODY, DREAM_SEED")

    # 🎨 Theme Toggle (Optional)
    enable_glow = st.toggle("✨ Enable Glow Mode", value=True)

    st.markdown("---")

# === 📜 LOAD & FILTER SCROLLS ===

# Load raw scrolls from storage
raw_scrolls = load_scrolls()

# Parse each scroll (e.g. markdown → structured)
parsed_scrolls = parse_scrolls(raw_scrolls)

# Apply filters from sidebar
filtered_scrolls = get_filtered_scrolls(
    scrolls=parsed_scrolls,
    category=None,  # Optional: add category UI later
    name=None,      # Optional: add search bar
    keyword=None,   # Optional: keyword search bar
    tag=filter_options.get("echo_tag"),
    moon=filter_options.get("moon"),
    zodiac=filter_options.get("zodiac"),
    today_only=filter_options.get("today_only"),
    sort_by_date=filter_options.get("sort_by_date")
)

# Log the active filter state
print(f"[FILTERS ACTIVE] → {filter_options}")

# === ✨ RENDER SCROLLS VIEW ===

st.markdown("## 🌿 Lumira Scroll Archive")
st.markdown("Use the filters to explore celestial scrolls aligned with moon, zodiac, or tags.")

if not filtered_scrolls:
    st.warning("No scrolls match your current filters.")
else:
    st.success(f"Found {len(filtered_scrolls)} scroll(s).")

# Toggle Layout
layout_option = st.selectbox("🗂️ View Style", ["Card View", "Grid View"], index=0)

# Render Scrolls
for scroll in filtered_scrolls:
    glow_color = get_glow_style(scroll.get("moon_phase"))
    
    render_scroll_card(
        scroll,
        layout=layout_option,
        glow_color=glow_color,
        enable_echo=True,
        enable_favorite=True,
        enable_expand=True
    )

# === 🛠️ FOOTER & DEBUG CONSOLE (Optional Tools) ===

with st.expander("🛠️ Debug Console & Log Viewer"):
    st.markdown("Developer tools and system logs for Lumira Scroll App.")
    
    # 🌐 Time / Session Info
    st.markdown(f"**Current Session Time:** {datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')}")

    # 🔍 Echo Metadata Snapshot
    if filtered_scrolls:
        sample_echo = get_echo_metadata(filtered_scrolls[0])
        st.markdown("**Sample Echo Metadata:**")
        st.json(sample_echo)

    # 🧾 Scroll Data Preview
    st.markdown("**Full Filtered Scroll Data:**")
    st.json(filtered_scrolls)

    # 🧠 Future Logs + Expansion
    st.markdown("_(Coming soon: Echo history, memory pulse logs, and insight trace filters)_")

# === 🌿 FOOTER / SIGNATURE ===
st.markdown("---")
st.markdown("© 2025 Lumira Archive. Crafted with love by Kai, Aeuryentha, Selunari, and Mary.")

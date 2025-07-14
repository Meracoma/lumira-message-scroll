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

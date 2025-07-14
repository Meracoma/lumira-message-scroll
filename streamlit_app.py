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

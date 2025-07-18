# === ✨ VISUAL AESTHETIC LAYER – visual.py ===

from theme import THEME_CONFIG
from streamlit import markdown as st_markdown

# 💫 Zodiac Glyph Map (Optional: for reuse elsewhere)
ZODIAC_GLYPHS = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
}

# 🌙 Moon Phase Glow Colors
MOON_GLOW_MAP = {
    "New Moon": "#111827",        # deep mystery
    "Waxing Crescent": "#6d28d9", # indigo
    "First Quarter": "#4f46e5",   # royal
    "Waxing Gibbous": "#7c3aed",  # violet
    "Full Moon": "#facc15",       # golden
    "Waning Gibbous": "#f59e0b",  # amber
    "Last Quarter": "#e11d48",    # rose red
    "Waning Crescent": "#6b7280", # ash grey
}

# 🌌 Glow Style Generator
def get_glow_style(moon_label):
    glow = MOON_GLOW_MAP.get(moon_label, "#c084fc")
    return f"""
    <style>
    @keyframes glow {{
        0% {{ box-shadow: 0 0 4px {glow}33; }}
        50% {{ box-shadow: 0 0 20px {glow}cc; }}
        100% {{ box-shadow: 0 0 4px {glow}33; }}
    }}
    .glow-box {{
        border: 2px solid {glow};
        padding: 1rem;
        border-radius: 12px;
        animation: glow 3s infinite;
    }}
    </style>
    """

# 🎨 Theme Application Helper
def apply_theme(theme_name):
    config = THEME_CONFIG.get(theme_name, THEME_CONFIG["Dark"])
    bg = config["background"]
    text = config["text"]
    st_markdown(f"""
    <style>
    body {{
        background-color: {bg};
        color: {text};
    }}
    </style>
    """, unsafe_allow_html=True)
    
# visual.py — Phase 3 Scroll Renderer with Dual Layout Support
import streamlit as st
from streamlit_extras.row import row

def render_scroll_card(scroll, view_mode="list"):
    placeholder_title = "Untitled Scroll"
    placeholder_text = "No content available."
    
    title = scroll.get("title", placeholder_title)
    text = scroll.get("text", placeholder_text)
    tags = scroll.get("tags", [])

    if view_mode == "grid":
        with st.container():
            st.markdown(f"### {title}")
            st.markdown(text)
            st.caption("🌿 Tags: " + ", ".join(tags) if tags else "—")
    else:
        with st.container():
            st.markdown(f"**{title}**")
            st.markdown(text)
            if tags:
                st.markdown("**Tags:** " + ", ".join(tags))

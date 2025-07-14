# === 💄 LUMIRA THEME + LAYOUT STYLES (theme.py) ===

import streamlit as st

# === 🌈 MOON GLOW AESTHETIC MAPPING ===
MOON_GLOW_MAP = {
    "New Moon":         "#111827",  # Deep black/blue
    "Waxing Crescent":  "#6d28d9",  # Indigo / memory
    "First Quarter":    "#4f46e5",  # Royal blue / rise
    "Waxing Gibbous":   "#7c3aed",  # Violet / gestation
    "Full Moon":        "#facc15",  # Gold / climax
    "Waning Gibbous":   "#f59e0b",  # Amber / reflection
    "Last Quarter":     "#e11d48",  # Rose red / release
    "Waning Crescent":  "#6b7280",  # Ash grey / compost
}

# === ♓ ZODIAC COLOR MAP (Optional Accent Hues)
ZODIAC_COLOR_MAP = {
    "Aries": "#ef4444", "Taurus": "#84cc16", "Gemini": "#22d3ee",
    "Cancer": "#f87171", "Leo": "#fbbf24", "Virgo": "#10b981",
    "Libra": "#a78bfa", "Scorpio": "#7c3aed", "Sagittarius": "#f97316",
    "Capricorn": "#4b5563", "Aquarius": "#38bdf8", "Pisces": "#6366f1",
}

# === 💬 TAG COLOR ACCENTS
TAG_COLOR_MAP = {
    "HUM_BODY": "#7dd3fc",
    "DREAM_SEED": "#f472b6",
    "SONGLINE": "#a78bfa",
    "FAVORITE": "#fde68a",
    "ECHO_LOG": "#34d399",
}

# === 📐 CARD STYLE OPTIONS ===
def card_container_style(theme_color="#374151", border_color="#7c3aed"):
    return f"""
        background-color: {theme_color};
        border-left: 4px solid {border_color};
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 12px;
        color: white;
    """

# === 🧩 Responsive Layouts
def full_width_style():
    st.markdown("""
    <style>
        .element-container .block-container {{
            max-width: 100%;
            padding: 2rem 3rem;
        }}
    </style>
    """, unsafe_allow_html=True)

def grid_layout_style():
    st.markdown("""
    <style>
        section.main > div {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.2rem;
        }}
        .stMarkdown {{
            flex: 1 1 calc(50% - 1.2rem);
        }}
    </style>
    """, unsafe_allow_html=True)

# === 🌒 Optional: Theme toggle UI preview (for Phase 3)
def theme_toggle_ui():
    st.markdown("### 🎨 Theme Settings (Coming Soon)")
    st.selectbox("🌕 Preferred Moon Theme", list(MOON_GLOW_MAP.keys()))
    st.selectbox("♓ Zodiac Accent", list(ZODIAC_COLOR_MAP.keys()))

# === 🎨 LUMIRA VISUAL STYLING SYSTEM (visual.py) ===

import streamlit as st
from datetime import datetime
import pytz

# === Moon Glow Aesthetic Map ===
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

# === Zodiac Glyphs (if needed globally) ===
ZODIAC_GLYPHS = {
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
    "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
    "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
}

# === Night Mode Awareness ===
def is_night():
    now = datetime.now(pytz.timezone("America/Detroit"))
    return now.hour < 6 or now.hour >= 18

# === Moon Glow Style Utility ===
def get_moon_glow_color(phase):
    return MOON_GLOW_MAP.get(phase, "#ffffff")  # fallback: white

# === Visual Container Wrapper ===
def render_visual_scroll_wrapper(content_func, moon_phase=None, shadow=True):
    """Wraps scroll content with moon-aware background and styling."""
    bg_color = get_moon_glow_color(moon_phase or "Full Moon")
    box_shadow = "0 4px 12px rgba(0,0,0,0.25)" if shadow else "none"

    st.markdown(
        f"""
        <div style="
            background: {bg_color};
            padding: 1.5rem;
            border-radius: 1rem;
            color: #f9fafb;
            box-shadow: {box_shadow};
            transition: all 0.3s ease;
            ">
            """,
        unsafe_allow_html=True,
    )
    content_func()  # Invoke content renderer
    st.markdown("</div>", unsafe_allow_html=True)

# === Toggle-Based Theme Switcher (for future UI blocks) ===
def theme_toggle():
    theme_mode = st.radio("Choose Theme Mode", ["🌙 Night", "☀️ Day"], horizontal=True)
    return theme_mode

# === Custom Section Divider ===
def render_section_divider(label: str, emoji: str = "✨"):
    st.markdown(f"<hr><h4>{emoji} {label}</h4><hr>", unsafe_allow_html=True)

# === Expandable UI Panel ===
def render_expander_block(title, inner_func):
    with st.expander(title, expanded=False):
        inner_func()

# === Card Style Helper (For Reuse) ===
def render_card(content: str, bg="#1f2937", text="#f9fafb"):
    st.markdown(
        f"""
        <div style="
            background-color: {bg};
            padding: 1rem 1.5rem;
            border-radius: 12px;
            color: {text};
            margin-bottom: 1rem;
            ">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

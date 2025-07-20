=== ✨ VISUAL AESTHETIC LAYER – visual.py === 

from theme import THEME_CONFIG from streamlit import markdown as st_markdown import streamlit as st from streamlit_extras.row import row

💫 Zodiac Glyph Map (Optional: for reuse elsewhere) 

ZODIAC_GLYPHS = { "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋", "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏", "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓" }

🌙 Moon Phase Glow Colors 

MOON_GLOW_MAP = { "New Moon": "#111827", "Waxing Crescent": "#6d28d9", "First Quarter": "#4f46e5", "Waxing Gibbous": "#7c3aed", "Full Moon": "#facc15", "Waning Gibbous": "#f59e0b", "Last Quarter": "#e11d48", "Waning Crescent": "#6b7280" }

🌌 Glow Style Generator 

def get_glow_style(moon_label): glow = MOON_GLOW_MAP.get(moon_label, "#c084fc") return f""" @keyframes glow {{ 0% {{ box-shadow: 0 0 4px {glow}33; }} 50% {{ box-shadow: 0 0 20px {glow}cc; }} 100% {{ box-shadow: 0 0 4px {glow}33; }} }} .glow-box {{ border: 2px solid {glow}; padding: 1rem; border-radius: 12px; animation: glow 3s infinite; }} """

🎨 Theme Application Helper 

def apply_theme(theme_name): config = THEME_CONFIG.get(theme_name, THEME_CONFIG["Dark"]) bg = config["background"] text = config["text"] st_markdown(f""" body {{ background-color: {bg}; color: {text}; }} """, unsafe_allow_html=True)

🌟 Scroll Renderer with Role + Emotion Styling 

def render_scroll_card(scroll, view_mode="list"): # Defaults placeholder_title = "Untitled Scroll" placeholder_text = "No content available."

# Fetch values title = scroll.get("title", placeholder_title) text = scroll.get("text", placeholder_text) tags = scroll.get("tags", []) # Role + emotion sync from session config (Block 10) config = st.session_state.get("scroll_config", {}) role_class = config.get("user_role", "dreamer") emotion_class = f"emotion-{config.get('emotion_state', 'neutral')}" # Begin scroll card container with custom classes st.markdown(f"<div class='scroll-card {role_class} {emotion_class}'>", unsafe_allow_html=True) if view_mode == "grid": with st.container(): st.markdown(f"### {title}") st.markdown(text) st.caption("🌿 Tags: " + ", ".join(tags) if tags else "—") else: with st.container(): st.markdown(f"**{title}**") st.markdown(text) if tags: st.markdown("**Tags:** " + ", ".join(tags)) st.markdown("</div>", unsafe_allow_html=True) 

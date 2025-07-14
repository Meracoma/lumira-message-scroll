# === 🌠 VISUAL RENDER SYSTEM (visual.py) ===

import streamlit as st
from theme import MOON_GLOW_MAP, ZODIAC_GLYPHS
from datetime import datetime

def get_scroll_color(scroll):
    """Get background color based on moon phase or category aesthetic."""
    moon = scroll.get("moon_phase", "New Moon")
    return MOON_GLOW_MAP.get(moon, "#1f2937")

def render_constellation_card(scroll, layout="full", show_tags=True):
    """Render a single scroll in full or grid layout."""
    bg_color = get_scroll_color(scroll)
    tags = scroll.get("tags", [])
    tag_links = "  ".join([f"[#{tag}](#)" for tag in tags]) if show_tags else ""

    with st.container():
        st.markdown(f"""
        <div style="background-color:{bg_color}; padding:1.2em; border-radius:1em; color:white;">
            <h3 style="margin-bottom:0;">🌌 {scroll.get("name", "Untitled")}</h3>
            <p style="margin-top:0;"><em>{scroll.get("zodiac", "—")} · {scroll.get("moon_phase", "—")}</em></p>
            <p>{scroll.get("message", "")}</p>
            <div style="font-size:0.9em; color:#d1d5db;">{tag_links}</div>
        </div>
        """, unsafe_allow_html=True)

        # Favorite & Echo options
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⭐ Save to Favorites", key=f"fav_{scroll.get('id')}"):
                st.session_state.setdefault("favorites", []).append(scroll)
        with col2:
            if st.button("📣 Send to Echo Log", key=f"echo_{scroll.get('id')}"):
                st.session_state.setdefault("echo_log", []).append(scroll)

def render_scroll_layout(scrolls, layout="full"):
    """Render all scrolls in selected layout style."""
    for scroll in scrolls:
        render_constellation_card(scroll, layout=layout)

def tag_click_filter(tag):
    """Handle interactive tag click to rerun filters."""
    st.session_state["selected_tag"] = tag
    st.experimental_rerun()


# === scroll_view_main.py – Lumira Scroll View Core ===

import streamlit as st
from configure import MOON_GLOW_MAP, ZODIAC_SIGNS, TIMEZONE, PROJECT_NAME
from filters import (
    filter_by_keyword,
    filter_by_category,
    filter_by_name,
    filter_by_tag,
    filter_by_date_range
)
from utils import get_moon_phase_label, get_zodiac_sign
from visual import render_constellation_card
from storage import load_messages


# === UI: Scroll Filter Panel ===
def show_filter_panel():
    st.markdown("## 🔍 Refine Your Scrolls")

    with st.expander("🎛️ Filters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input("🔑 Keyword")
            name_filter = st.text_input("📛 Name Filter")
            tag_filter = st.text_input("🏷️ Tag Filter")
            category_filter = st.selectbox("🗂️ Category", ["All", "Dream", "Message", "Echo", "Vision"])

        with col2:
            moon_filter = st.selectbox("🌕 Moon Phase", ["All", "New Moon", "Waxing Crescent", "First Quarter", 
                                                        "Waxing Gibbous", "Full Moon", "Waning Gibbous", 
                                                        "Last Quarter", "Waning Crescent"])
            zodiac_filter = st.selectbox("♈ Zodiac Sign", ["All", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                                                            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
            sort_by = st.radio("📅 Sort By", ["Newest First", "Oldest First"])
            date_range = st.date_input("🗓️ Date Range", [datetime(2024, 1, 1), datetime.now()])

    filters = {
        "keyword": keyword,
        "name": name_filter,
        "tag": tag_filter,
        "category": category_filter,
        "moon": moon_filter,
        "zodiac": zodiac_filter,
        "sort": sort_by,
        "date_range": date_range,
    }

    print(f"[UI] Filters set: {filters}")
    return filters


# === Core Render + Filtering ===
def show_scroll_view():
    scrolls = load_messages()
    print(f"[LOAD] Loaded {len(scrolls)} scroll(s)")

    filters = show_filter_panel()

    # Apply filters
    if filters["category"] != "All":
        scrolls = filter_by_category(scrolls, filters["category"])
    scrolls = filter_by_keyword(scrolls, filters["keyword"])
    scrolls = filter_by_name(scrolls, filters["name"])
    scrolls = filter_by_tag(scrolls, filters["tag"])

    # Filter by date
    start_date, end_date = filters["date_range"]
    scrolls = filter_by_date_range(scrolls, start_date, end_date)

    # Moon + Zodiac filter
    if filters["moon"] != "All":
        scrolls = [s for s in scrolls if s.get("moon_phase") == filters["moon"]]
        print(f"[FILTER] Moon Phase: {filters['moon']} → {len(scrolls)} result(s)")
    if filters["zodiac"] != "All":
        scrolls = [s for s in scrolls if s.get("zodiac_sign") == filters["zodiac"]]
        print(f"[FILTER] Zodiac Sign: {filters['zodiac']} → {len(scrolls)} result(s)")

    # Sort
    scrolls = sorted(scrolls, key=lambda x: x["timestamp"], reverse=(filters["sort"] == "Newest First"))
    print(f"[SORT] Order: {filters['sort']} → {len(scrolls)} total sorted")

    # === Display ===
    st.markdown("## 🪶 Scrolls")

    if not scrolls:
        st.info("No scrolls match your filters.")
        print("[INFO] No matching scrolls")
    else:
        for scroll in scrolls:
            moon_label = scroll.get("moon_phase", "Full Moon")
            sign = scroll.get("zodiac_sign", "Cancer")
            html = render_constellation_card(scroll, moon_label, sign)
            st.markdown(html, unsafe_allow_html=True)
            # future: include toggle for ⭐ Save or 📣 Echo

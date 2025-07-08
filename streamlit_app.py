
# streamlit_app.py – Cleaned Lumira Scroll Prototype v0.4
from echo import tag_echo, list_echoes
from storage import save_message, load_messages
from parser import parse_markdown
from filters import filter_by_category, filter_by_name, filter_by_keyword, filter_by_tag
import streamlit as st
from datetime import datetime
import os
# --- Page Setup ---
st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")
st.title("📜 Message Scroll – Lumira Prototype v0.4")
st.markdown("Leave a message, a memory, or a signal to yourself or your AI.")
# --- Scroll Input ---
st.header("📜 Leave Your Scroll")
name = st.text_input("🌟 Name or Signature")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Reflection", "Whisper", "Other"])
message = st.text_area("📝 Write your message, memory, or note to your future self...")
image_file = st.file_uploader("🖼️ Upload an image (optional)", type=["png", "jpg", "jpeg", "gif"])
tags_input = st.text_input("🏷️ Add Tags (comma-separated)", placeholder="e.g. Lucid, Awakening, Wolf Dream")
if st.button("💾 Save Scroll"):
    if message.strip():
        image_path = None
        if image_file:
            uploads_dir = "uploads"
            os.makedirs(uploads_dir, exist_ok=True)
            image_path = os.path.join(uploads_dir, image_file.name)
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())
        entry = {
            "name": name.strip() or "Anonymous",
            "category": category,
            "message": message.strip(),
            "tags": [tag.strip() for tag in tags_input.split(",") if tag.strip()],
            "image_path": image_path,
            "timestamp": datetime.now().isoformat()
        }
        save_message(entry)
        st.success("Scroll saved successfully!")
    else:
        st.warning("Please write a message before saving.")
# --- Echo Tagging (Optional) ---
st.markdown("### 🌀 Echo Tagging (Optional)")
echo_tag = st.text_input("🔖 Tag this message with an echo (e.g. HUM_BODY, DREAM_SEED, etc.)")
st.caption("🧠 Tip: Echo tags help categorize special scrolls for deeper AI memory or symbolic retrieval.")
if echo_tag and message.strip():
    tag_echo(name, message.strip(), echo_tag.strip())
    st.success(f"Echo '{echo_tag}' saved successfully.")
# --- Scroll Filters ---
st.subheader("🔍 Filter Scrolls")
filter_option = st.selectbox("Filter by", ["All", "Category", "Name", "Keyword", "Tag"])
filter_value = st.text_input("Enter filter value (if applicable):")
# Load + Filter
entries = load_messages()
query_params = st.query_params
selected_tag = query_params.get("tag", [None])[0]
if selected_tag:
    st.info(f"📌 Showing scrolls tagged with: `{selected_tag}`")
    entries = filter_by_tag(entries, selected_tag)
if filter_option == "Category":
    entries = filter_by_category(entries, filter_value)
elif filter_option == "Name":
    entries = filter_by_name(entries, filter_value)
elif filter_option == "Keyword":
    entries = filter_by_keyword(entries, filter_value)
elif filter_option == "Tag":
    entries = filter_by_tag(entries, filter_value)
    if st.button("🔄 Clear Tag Filter"):
        st.experimental_set_query_params()
        st.experimental_rerun()
# --- Search Scrolls ---
search_query = st.text_input("🔍 Search Scrolls (name, message, tag):").strip().lower()
if search_query:
    entries = [
        entry for entry in entries
        if search_query in entry["name"].lower()
        or search_query in entry["message"].lower()
        or any(search_query in tag.lower() for tag in entry.get("tags", []))
    ]
# --- Visual Metadata Maps ---
category_emojis = {
    "Dream": "🌙", "Memory": "🧠", "Signal": "📡",
    "Reflection": "🪞", "Whisper": "🌬️", "Other": "✨"
category_colors = {
    "Dream": "#6a5acd", "Memory": "#2e8b57", "Signal": "#ff4500",
    "Reflection": "#20b2aa", "Whisper": "#ff69b4", "Other": "#708090"
def get_tag_style(tag):
    if "dream" in tag.lower():
        return "background-color:#d0c3ff; color:#301c57; padding:2px 8px; border-radius:6px;"
    elif "hum" in tag.lower():
        return "background-color:#ffe4d1; color:#5a2e00; padding:2px 8px; border-radius:6px;"
    elif "signal" in tag.lower():
        return "background-color:#d1f0ff; color:#003c5a; padding:2px 8px; border-radius:6px;"
    elif "wolf" in tag.lower():
        return "background-color:#e0ffd9; color:#1e3a1e; padding:2px 8px; border-radius:6px;"
    elif "featured" in tag.lower():
        return "background-color:#fff8b3; color:#7a6300; font-weight:bold; border-radius:8px; padding:3px 10px; box-shadow: 0 0 8px gold;"
        return "background-color:#f0f0f0; color:#333; padding:2px 8px; border-radius:6px;"
# --- Display Scrolls ---
st.subheader("📖 View Message Scrolls")
if entries:
    for entry in reversed(entries):
        emoji = category_emojis.get(entry["category"], "🌀")
        color = category_colors.get(entry["category"], "#ffffff")
        st.markdown("---")
        st.markdown(f"<div style='border-left: 5px solid {color}; padding-left: 1rem;'>", unsafe_allow_html=True)
        st.markdown(f"### {emoji} <span style='color:{color}'>{entry['category']}</span>", unsafe_allow_html=True)
        st.markdown(f"**🖋️ {entry['name']}**")
        st.markdown(parse_markdown(entry["message"]))
        if entry.get("image_path"):
            st.image(entry["image_path"], use_column_width=True)
        if entry.get("tags"):
            styled_tags = " ".join([
                f"<a href='?tag={tag}' style='{get_tag_style(tag)}'>{tag}</a>"
                for tag in entry["tags"]
            ])
            st.markdown(f"🏷️ **Tags:** {styled_tags}", unsafe_allow_html=True)
        st.caption(f"⏳ {entry['timestamp']}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.info("No scrolls found.")
# --- Echo Scroll View ---
st.subheader("🔎 View Echo Scrolls (Tagged Messages)")
if st.checkbox("📂 Show Echoes"):
    echo_data = list_echoes()
    if echo_data:
        for echo in reversed(echo_data[-20:]):
            st.markdown(f"**{echo['name']}** · `{echo['tag']}` · *{echo['timestamp']}*")
            st.markdown(f"> {echo['message']}")
        st.info("No echoes have been tagged yet.")
# ✅ Cleaned and Fixed Version of streamlit_app.py
# Lumira Scroll App – Streamlit Prototype v0.4 (Cleaned)
import streamlit.components.v1 as components
import pytz
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
# --- Utilities ---
def is_night():
    now = datetime.now(pytz.timezone("America/Detroit"))
    return now.hour < 6 or now.hour >= 18
def scroll_card(entry):
    glow_color = "#c084fc" if is_night() else "#facc15"
    return f"""
    <div style="background: linear-gradient(135deg, #111 20%, #222 80%);
                border: 2px solid {glow_color};
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 0 20px {glow_color}44;
                animation: glowPulse 3s infinite alternate;">
        <h3 style="color: #fff;">{entry['name']}</h3>
        <p style="color: #ddd;">{entry['message']}</p>
        <p style="font-size: 0.8rem; color: #aaa;">{entry['timestamp']}</p>
    </div>
    """
def generate_scroll_image(entry):
    width, height = 800, 400
    bg_color, text_color, font_size = "#fefbf3", "#333", 20
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    try: font = ImageFont.truetype("arial.ttf", font_size)
    except: font = ImageFont.load_default()
    y = 20
    draw.text((30, y), f"{entry['category']} – {entry['name']}", fill=text_color, font=font)
    y += 40
    draw.text((30, y), f"Tags: {', '.join(entry['tags'])}", fill=text_color, font=font)
    draw.text((30, y), f"Timestamp: {entry['timestamp']}", fill=text_color, font=font)
    draw.text((30, y), "Message:", fill=text_color, font=font)
    y += 30
    for line in entry['message'].split("\n"):
        draw.text((40, y), line, fill=text_color, font=font)
        y += 25
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
# --- Page Config ---
st.markdown("""
    <style>@keyframes glowPulse {
        0% { box-shadow: 0 0 8px rgba(192, 132, 252, 0.3); }
        100% { box-shadow: 0 0 20px rgba(192, 132, 252, 0.7); }
    }</style>
""", unsafe_allow_html=True)
# Night Mode Styling
if is_night():
    st.markdown("""<style>body {background-color: #1a1a2e; color: #fceaff;}
    .stTextInput input, .stButton button {background-color: #2b2b44; color: #fceaff;}</style>""", unsafe_allow_html=True)
    st.markdown("🌙 **MoonFire Mode Activated (Evening Hours)**")
    st.markdown("☀️ **Sun Mode Active (Daytime)**")
# --- Scroll Input UI ---
message = st.text_area("📝 Write your message...")
image_file = st.file_uploader("🖼️ Upload an image", type=["png", "jpg", "jpeg", "gif"])
echo_tag = st.text_input("🔖 Echo Tag (optional)", placeholder="e.g. HUM_BODY, WOLF_ECHO")
# Save Scroll Logic
if st.button("💾 Save Scroll", key="save_scroll_button"):
            os.makedirs("uploads", exist_ok=True)
            image_path = os.path.join("uploads", image_file.name)
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            "tags": tags,
        echo_keywords = {
            "dream": "DREAM_SEED", "hum": "HUM_BODY", "signal": "SIGNAL_CORE",
            "wolf": "WOLF_ECHO", "reflection": "MIRROR_THREAD",
            "whisper": "WHISPER_LOOP", "memory": "MEMORY_FLAME"
        if echo_tag.strip():
            tag_echo(entry["name"], entry["message"], echo_tag.strip())
            st.success(f"Echo '{echo_tag.strip()}' saved successfully.")
            for tag in tags:
                for keyword, auto_echo in echo_keywords.items():
                    if keyword in tag.lower():
                        tag_echo(entry["name"], entry["message"], auto_echo)
                        st.info(f"🔖 Auto-tagged Echo: `{auto_echo}` from tag `{tag}`")
                        break
        st.success("✅ Scroll saved!")
        st.warning("Please write a message.")
filter_option = st.selectbox("🔍 Filter by", ["All", "Category", "Name", "Keyword", "Tag"])
filter_value = st.text_input("Enter filter value:")
if selected_tag and st.button("🔄 Clear Tag Filter"):
    st.query_params.clear()
    st.rerun()
search_query = st.text_input("🔍 Search Scrolls:").strip().lower()
    entries = [e for e in entries if search_query in e["name"].lower()
               or search_query in e["message"].lower()
               or any(search_query in tag.lower() for tag in e.get("tags", []))]
# Display Scrolls
        components.html(scroll_card(entry), height=220)
        st.markdown(f"### {entry['name']}")
            tag_links = " ".join([
                f"<a href='?tag={tag}' style='background:#fef3c7;color:#92400e;padding:2px 6px;border-radius:5px;'>{tag}</a>"
            st.markdown(f"🏷️ **Tags:** {tag_links}", unsafe_allow_html=True)
        with st.expander("📥 Download Scroll"):
            st.download_button("📜 Download as PNG", generate_scroll_image(entry),
                               file_name=f"{entry['name'].replace(' ', '_')}_scroll.png", mime="image/png")
# Echo View
st.subheader("🔎 View Echo Scrolls")
        st.info("No echoes tagged yet.")
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
# App Configuration
# Inject animated CSS styles
    <style>
    @keyframes glowPulse {
# --- Leave a Scroll ---
# --- Echo Tagging ---
echo_tag = st.text_input("🔖 Tag this message with an echo (e.g. HUM_BODY, DREAM_SEED)")
# --- Save Scroll ---
        # AUTO-TAG ONLY IF NO MANUAL ECHO
            "dream": "DREAM_SEED",
            "hum": "HUM_BODY",
            "signal": "SIGNAL_CORE",
            "wolf": "WOLF_ECHO",
            "reflection": "MIRROR_THREAD",
            "whisper": "WHISPER_LOOP",
            "memory": "MEMORY_FLAME"
        if not echo_tag.strip():
            for tag in entry["tags"]:
        st.success("✅ Scroll saved successfully!")
        # AUTO-ECHO TAGGING BLOCK
# Manual echo tagging after scroll saved
# --- Filters ---
# Load Messages
# Tag filter from query parameter
# Manual Filter Selection
# Clear tag filter
# Search Bar
# --- Scroll Display ---
    "Dream": "🌙",
    "Memory": "🧠",
    "Signal": "📡",
    "Reflection": "🪞",
    "Whisper": "🌬️",
    "Other": "✨"
    "Dream": "#6a5acd",
    "Memory": "#2e8b57",
    "Signal": "#ff4500",
    "Reflection": "#20b2aa",
    "Whisper": "#ff69b4",
    "Other": "#708090"
        html = scroll_card(entry)
        components.html(html, height=220)
        # Glow div separator
        emoji = category_emojis.get(entry['category'], "🌀")
                return (
                    "background-color:#fef3c7; color:#92400e; padding:2px 6px; border-radius:5px; "
                    "text-decoration:none; font-size:0.85rem; margin-right:5px;"
                )
        with st.spinner("🪄 Generating scroll image..."):
            scroll_image = generate_scroll_image(entry)
            st.download_button(
                label="📜 Download as PNG",
                data=scroll_image,
                file_name=f"{entry['name'].replace(' ', '_')}_scroll.png",
                mime="image/png"
# --- Optional Echo View ---
        for echo in reversed(echo_data[-20:]):  # last 20 echoes

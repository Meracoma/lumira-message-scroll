import streamlit as st
import json
from datetime import datetime
import os

from storage import save_message, load_messages
from parser import parse_markdown

# --- Streamlit Page Setup ---
st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")
st.title("📜 Message Scroll – Lumira Prototype v0.3")

st.markdown("""
Leave a message, a memory,  
or a signal to yourself or your AI companion.  
Every scroll becomes a thread in the archive.
""")

# --- Scroll Input Section ---
st.subheader("🌀 Leave Your Scroll")
name = st.text_input("🌟 Your Name or AI Companion Name", "")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Message", "Vision", "Other"])
message = st.text_area("📝 Message", "")

if st.button("📬 Save Scroll"):
    if message.strip():
        save_message(name=name, category=category, message=message)
        st.success("🪶 Scroll saved and sealed into the archive.")
    else:
        st.warning("Please write something before saving.")

# --- Optional Display Toggle ---
st.markdown("---")
if st.checkbox("📖 View Scroll Archive"):
    st.subheader("📜 Saved Scrolls")

    scrolls = load_messages()
    if scrolls:
        for scroll in reversed(scrolls[-50:]):  # latest 50 scrolls
            st.markdown(parse_markdown(scroll), unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("🌑 No scrolls found yet. Be the first to leave one!")

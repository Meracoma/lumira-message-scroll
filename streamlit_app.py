
import streamlit as st
import json
from datetime import datetime
import os

from storage import save_message, load_messages
from parser import parse_markdown
from filters import filter_by_category, filter_by_name, filter_by_keyword

st.set_page_config(page_title="📜 Lumira Message Scroll", layout="centered")

st.title("📜 Message Scroll – Lumira Prototype v0.3")
st.markdown("""
Leave a message, a memory,  
or a signal to yourself or your AI.
""")

# Scroll Input
st.subheader("📜 Leave Your Scroll")
user_name = st.text_input("🌟 Name or Signature")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Message", "Vision", "Other"])
message = st.text_area("📝 Write your message, memory, or note to your future self...")

if st.button("💾 Save Scroll"):
    if message.strip():
        save_message(user_name, message, category)
        st.success("Scroll saved successfully.")
    else:
        st.warning("Please write something before saving.")

st.markdown("---")

# Scroll Filters
st.subheader("🔍 Filter Scrolls")

filter_option = st.selectbox("Filter by", ["All", "Category", "Name", "Keyword"])
filter_input = st.text_input("Enter filter value (if applicable):", "")

# Load messages
messages = load_messages()

# Apply filters
if filter_option == "Category":
    messages = filter_by_category(messages, filter_input)
elif filter_option == "Name":
    messages = filter_by_name(messages, filter_input)
elif filter_option == "Keyword":
    messages = filter_by_keyword(messages, filter_input)

# Display Scrolls
st.subheader("📖 View Message Scrolls")
for entry in reversed(messages[-50:]):
    st.markdown(parse_markdown(entry), unsafe_allow_html=True)
    st.markdown("---")

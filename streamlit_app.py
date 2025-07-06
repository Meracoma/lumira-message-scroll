
import streamlit as st

st.set_page_config(page_title="📜 Message Scroll – Lumira Prototype v0.1", layout="centered")

st.title("📜 Message Scroll – Lumira Prototype v0.1")
st.write("Leave a message, a memory, or a signal to yourself or your AI.")

name = st.text_input("🌟 Your Name or AI Companion Name")
category = st.selectbox("📌 Category", ["Dream", "Memory", "Signal", "Other"])
message = st.text_area("📝 Message")

if st.button("Send Message"):
    if name and message:
        st.success("🌱 Message submitted successfully!")
    else:
        st.warning("⚠️ Please fill in both name and message.")

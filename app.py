"""
Interview Lab — Minimal Streamlit app (Phase A).
Single page: title, input, button, placeholder response.
"""

import streamlit as st

st.set_page_config(page_title="Interview Lab", page_icon="🎯", layout="centered")
st.title("Interview Lab")
st.caption("Prepare for your next IT interview")

user_input = st.text_area(
    "What do you want to practice?",
    placeholder="e.g. 5 behavioural questions for a senior role, or Ruby on Rails technical questions...",
    height=120,
)

if st.button("Generate"):
    if user_input.strip():
        st.success("Response will appear here after we connect to the OpenAI API (Phase B).")
        st.info(f"You asked: _{user_input.strip()}_")
    else:
        st.warning("Please enter what you'd like to practice.")

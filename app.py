"""
Interview Lab — Streamlit app (Phase B: OpenAI integration).
Single page: user input, one system prompt, call OpenAI, show response.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Interview Lab", page_icon="🎯", layout="centered")
st.title("Interview Lab")
st.caption("Prepare for your next IT interview")

# One system prompt: IT interview coach (Phase B)
SYSTEM_PROMPT = """You are an IT interview coach. Help the user prepare for job interviews.
You can help with:
- Behavioural questions (e.g. STAR method, past experience, culture fit).
- Technical questions (e.g. programming, system design, Ruby on Rails, or other technologies).
- Questions the candidate should ask the interviewer at the end.
- Custom prep (e.g. tailoring to a role or job description).
Be concise, practical, and supportive. Answer in clear paragraphs or bullet points as appropriate."""

user_input = st.text_area(
    "What do you want to practice?",
    placeholder="e.g. 5 behavioural questions for a senior role, or Ruby on Rails technical questions...",
    height=120,
)

if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter what you'd like to practice.")
        st.stop()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key is missing. Add OPENAI_API_KEY to your .env file.")
        st.stop()

    with st.spinner("Generating..."):
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input.strip()},
                ],
            )
            reply = response.choices[0].message.content
            st.success("Here’s your interview prep:")
            st.markdown(reply)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

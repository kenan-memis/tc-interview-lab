"""
Interview Lab — Streamlit app (Phase C: interview prep focus in UI).
Single page: practice type dropdown, user input, one system prompt, call OpenAI, show response.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Interview Lab", page_icon="🎯", layout="centered")
st.title("Interview Lab")
st.caption("Prepare for your next IT interview")

# Practice type options (Phase C)
PRACTICE_TYPES = {
    "Behavioural": {
        "label": "Behavioural",
        "placeholder": "e.g. 5 STAR-method questions for a senior role, or tell me about a conflict with a colleague",
        "tip": "Focus on past behaviour, impact, and how you’d apply the STAR method.",
    },
    "Technical": {
        "label": "Technical",
        "placeholder": "e.g. Ruby on Rails interview questions, or system design for a mid-level backend role",
        "tip": "Specify language/framework (e.g. Ruby, Rails) or topic (algorithms, system design) for better prep.",
    },
    "Questions to ask them": {
        "label": "Questions to ask them",
        "placeholder": "e.g. questions to ask a CTO, or what to ask at the end of a product manager interview",
        "tip": "Ask for questions that show curiosity and fit without sounding generic.",
    },
    "Custom": {
        "label": "Custom",
        "placeholder": "e.g. paste a job description and ask to prepare, or mix behavioural + technical for a specific role",
        "tip": "Paste a job description or describe the role for tailored prep.",
    },
}

# One system prompt: IT interview coach (Phase B)
SYSTEM_PROMPT = """You are an IT interview coach. Help the user prepare for job interviews.
You can help with:
- Behavioural questions (e.g. STAR method, past experience, culture fit).
- Technical questions (e.g. programming, system design, Ruby on Rails, or other technologies).
- Questions the candidate should ask the interviewer at the end.
- Custom prep (e.g. tailoring to a role or job description).
Be concise, practical, and supportive. Answer in clear paragraphs or bullet points as appropriate."""

practice_type = st.selectbox(
    "What do you want to practice?",
    options=list(PRACTICE_TYPES.keys()),
    index=0,
    help="Choose the kind of interview prep you need.",
)

config = PRACTICE_TYPES[practice_type]
st.caption(config["tip"])

user_input = st.text_area(
    "Your request (add details below)",
    placeholder=config["placeholder"],
    height=120,
    key="user_request",
)

if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter what you'd like to practice.")
        st.stop()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key is missing. Add OPENAI_API_KEY to your .env file.")
        st.stop()

    # Send category + user text so the coach can tailor the response (Phase C)
    user_message = f"[{practice_type}] {user_input.strip()}"

    with st.spinner("Generating..."):
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            reply = response.choices[0].message.content
            st.success("Here’s your interview prep:")
            st.markdown(reply)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

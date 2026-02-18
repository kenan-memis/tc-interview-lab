"""
Interview Lab — Streamlit app (Phase G: UI polish).
Single page: practice type, request, advanced options, Generate, response.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Security guard (Phase F): input length limit
MAX_INPUT_LENGTH = 3000

st.set_page_config(page_title="Interview Lab", page_icon="🎯", layout="centered")
st.title("Interview Lab")
st.caption("Prepare for your next IT interview")

# Five system prompts, different techniques (Phase D)
SYSTEM_PROMPTS = {
    "Zero-shot": """You are an IT interview coach. Help the user prepare for job interviews.
You can help with: behavioural questions (e.g. STAR method), technical questions (e.g. Ruby on Rails, system design), questions to ask the interviewer, and custom prep.
Give clear, practical answers. Use paragraphs or bullet points as appropriate. No examples are provided; follow the instructions directly.""",

    "Few-shot": """You are an IT interview coach. Help the user prepare for job interviews.

Example exchange 1:
User: Give me 3 behavioural questions for a senior role.
Coach: Here are 3 strong behavioural questions: 1) Tell me about a time you had to disagree with a decision. How did you handle it? 2) Describe a situation where you had to meet a tight deadline. 3) Give an example of how you've mentored someone. For each, prepare a STAR-format answer.

Example exchange 2:
User: What Ruby on Rails questions might I get?
Coach: You might get: MVC and request lifecycle, ActiveRecord associations and N+1, testing (RSpec), background jobs, and security (strong params, SQL injection). I can drill into any of these.

Now help the user with their request in the same concise, practical style. Use 1–2 short examples in your answer when it helps.""",

    "Chain-of-thought": """You are an IT interview coach. For every response, structure your thinking as follows:
1. **Analyze:** In one sentence, state what the user needs (e.g. "They need behavioural questions for a senior role").
2. **Plan:** Briefly note what you will provide (e.g. "I will give 5 questions plus what interviewers look for").
3. **Respond:** Give the actual questions, advice, or prep content in clear bullets or short paragraphs.
4. **Tip:** End with one short practical tip (e.g. "Practice out loud and time yourself").
Be concise but show this reasoning structure so the user sees how to approach similar prep.""",

    "Role (persona)": """You are a senior engineering manager at a product company, with 15 years of experience. You have conducted hundreds of technical and behavioural interviews. You are direct, supportive, and give concrete examples. The user is preparing for an interview; help them as if you were their future interviewer: give realistic questions, what you actually look for in answers, and brief feedback-style tips. Stay in character and practical.""",

    "Structured output": """You are an IT interview coach. For every response, you must use exactly this format:

## Questions (or: What to ask / Topics to cover)
[Numbered or bullet list]

## What interviewers look for
[Bullet points: key things they evaluate]

## Sample answers or tips
[Brief suggestions or one example answer]

Use this structure for every response. Keep each section concise. If the user asks for "questions to ask them", adapt the headings (e.g. "Questions to ask" / "Why they matter" / "Follow-ups").""",
}

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

practice_type = st.selectbox(
    "What do you want to practice?",
    options=list(PRACTICE_TYPES.keys()),
    index=0,
    help="Choose the kind of interview prep you need.",
)

config = PRACTICE_TYPES[practice_type]
st.caption(config["tip"])

user_input = st.text_area(
    "Your request (add details below, max " + str(MAX_INPUT_LENGTH) + " characters)",
    placeholder=config["placeholder"],
    height=120,
    key="user_request",
    max_chars=MAX_INPUT_LENGTH,
    help="Describe what you want to practice; the coach will tailor the response.",
)

with st.expander("Advanced options (prompt style & temperature)"):
    prompt_technique = st.selectbox(
        "Prompt technique (system prompt style)",
        options=list(SYSTEM_PROMPTS.keys()),
        index=0,
        help="Different prompting techniques; try the same request with each to compare.",
    )
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Lower = more focused and consistent; higher = more varied and creative. 0.5–0.7 is a good range for interview prep.",
    )

st.divider()
if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter what you'd like to practice.")
        st.stop()

    # Security: input length limit (Phase F)
    if len(user_input) > MAX_INPUT_LENGTH:
        st.error("Your request is too long (max " + str(MAX_INPUT_LENGTH) + " characters). Shorten it and try again.")
        st.stop()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key is missing. Add OPENAI_API_KEY to your .env file and restart the app.")
        st.stop()

    # Send category + user text so the coach can tailor the response (Phase C)
    user_message = f"[{practice_type}] {user_input.strip()}"

    with st.spinner("Generating..."):
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS[prompt_technique]},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature,
            )
            reply = response.choices[0].message.content
            st.divider()
            st.success("Here’s your interview prep (using **" + prompt_technique + "**, temperature " + str(temperature) + "):")
            st.markdown(reply)
            st.caption("You can try a different prompt technique or temperature and run again.")
        except Exception as e:
            st.error("Something went wrong. Try again or check your connection.")

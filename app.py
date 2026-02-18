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
# Rate limiting (Top 5 improvement #5): max requests per session
MAX_REQUESTS_PER_SESSION = 20

st.set_page_config(page_title="Interview Lab", page_icon="🎯", layout="centered")
st.title("Interview Lab")
st.caption("Prepare for your next IT interview")

# Response style: user-facing label -> internal key (Top 5 improvement #1)
RESPONSE_STYLE_OPTIONS = [
    ("Direct answer", "Zero-shot"),
    ("With examples", "Few-shot"),
    ("Step-by-step reasoning", "Chain-of-thought"),
    ("Senior manager perspective", "Role (persona)"),
    ("Structured template", "Structured output"),
]
RESPONSE_STYLE_DISPLAY_TO_KEY = {display: key for display, key in RESPONSE_STYLE_OPTIONS}

# Five system prompts, different techniques (Phase D); keys = internal names
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

    "Chain-of-thought": """You are an IT interview coach. For every response, reason step-by-step internally (analyze what the user needs, plan what to provide, then formulate your answer). Do NOT show your reasoning steps in the output. Only output the final answer in a clean, structured form: give the actual questions, advice, or prep content in clear bullets or short paragraphs, and end with one short practical tip. Be concise.""",

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

with st.expander("Advanced options (response style & temperature)"):
    response_style_display = st.selectbox(
        "Response style",
        options=[opt[0] for opt in RESPONSE_STYLE_OPTIONS],
        index=0,
        help="How the coach should answer; try the same request with each to compare.",
    )
    prompt_technique = RESPONSE_STYLE_DISPLAY_TO_KEY[response_style_display]
    # Temperature presets (Top 5 improvement #2): simpler than raw slider
    TEMPERATURE_PRESETS = [
        ("Precise (0.2)", 0.2),
        ("Balanced (0.7)", 0.7),
        ("Creative (0.9)", 0.9),
    ]
    temp_choice = st.selectbox(
        "Temperature",
        options=[p[0] for p in TEMPERATURE_PRESETS],
        index=1,
        help="Precise = more predictable; Balanced = mix of consistency and variety; Creative = more varied.",
    )
    temperature = next(v for label, v in TEMPERATURE_PRESETS if label == temp_choice)

st.divider()
if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter what you'd like to practice.")
        st.stop()

    # Rate limiting (Top 5 improvement #5)
    if "request_count" not in st.session_state:
        st.session_state.request_count = 0
    if st.session_state.request_count >= MAX_REQUESTS_PER_SESSION:
        st.error(f"Rate limit reached ({MAX_REQUESTS_PER_SESSION} requests per session). Refresh the page to start a new session.")
        st.stop()

    # Security: input length limit (Phase F)
    if len(user_input) > MAX_INPUT_LENGTH:
        st.error("Your request is too long (max " + str(MAX_INPUT_LENGTH) + " characters). Shorten it and try again.")
        st.stop()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key is missing. Add OPENAI_API_KEY to your .env file and restart the app.")
        st.stop()

    # Embed practice type in system prompt for stronger steering (Top 5 improvement #3)
    system_content = (
        f"The user wants **{practice_type}** preparation. Use this to tailor your response.\n\n"
        + SYSTEM_PROMPTS[prompt_technique]
    )
    user_message = user_input.strip()

    with st.spinner("Generating..."):
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature,
            )
            reply = response.choices[0].message.content
            st.session_state.request_count = st.session_state.get("request_count", 0) + 1
            st.divider()
            st.success("Here’s your interview prep (using **" + response_style_display + "**, " + temp_choice + "):")
            st.markdown(reply)
            st.caption("You can try a different response style or temperature and run again.")
        except Exception as e:
            st.error("Something went wrong. Try again or check your connection.")

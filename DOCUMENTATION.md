# Interview Lab — Project Documentation

This document supports the Sprint 1 evaluation criteria: core concepts, technical implementation, and reflection. Use it to study before your project presentation.

---

## 1. Project plan

### 1.1 Goal and scope

- **Project name:** Interview Lab  
- **Goal:** Single-page web app for interview preparation, powered by OpenAI API and prompt engineering.  
- **Stack:** Python, Streamlit, OpenAI API.  
- **Deadline:** March 2 — project complete, on GitHub, deployed, presentation done.

### 1.2 Mandatory requirements (must complete)

| # | Requirement | Planned approach |
|---|-------------|------------------|
| 1 | Research & define interview prep focus | Choose 1–2 concrete areas (e.g. behavioural questions, technical Ruby/Rails, "questions to ask", or job-description prep). Document choice here. |
| 2 | Front-end | Streamlit: layout, inputs, display of AI response. |
| 3 | OpenAI API key | Create key; store in `.env`; load via `os.getenv` or `python-dotenv`. Never commit key. |
| 4 | Model choice | Pick one: GPT-4.1, GPT-4.1 mini, GPT-4.1 nano, GPT-4o, GPT-4o mini. Document choice and reason. |
| 5 | ≥5 system prompts, different techniques | Implement 5 variants (e.g. zero-shot, few-shot, chain-of-thought, role-based, structured output). Compare and document which works best. |
| 6 | ≥1 OpenAI parameter tuned | Expose and tune at least one of: temperature, top_p, frequency_penalty, etc. Document effect. |
| 7 | ≥1 security guard | At least one of: input length limit, rate limit, basic prompt-injection checks, or cost cap. Document what and why. |

**Model choice (decided):** We use **GPT-4o mini**. It gives a good balance of quality, cost, and speed for interview prep; keeps iteration and demos affordable; and fits well if we add a “cost per request” optional feature later.

### 1.3 Optional tasks (if time; bonus = 2+ medium/hard)

- **Easy (candidates):** difficulty levels, short vs detailed answers, AI personas (strict/neutral/friendly), or critique from ChatGPT.  
- **Medium (candidates):** all OpenAI settings as UI, JSON output formats, deploy, cost display, job-description field (RAG-style), or second LLM as judge.  
- **Hard (candidates):** multi-turn chatbot UI, LangChain, or LLM-as-judge evaluation.  

Decide after core app works; document chosen options in Technical Implementation and Reflection.

### 1.4 Phases and timeline (Feb 17 → Mar 2)

| Phase | Focus | Target |
|-------|--------|--------|
| **A. Setup** | Project folder, `requirements.txt`, `.env.example`, minimal Streamlit app runs locally | Day 1–2 |
| **B. OpenAI integration** | One system prompt, one user prompt, call API, show response in UI | Day 2–3 |
| **C. Interview prep focus** | Lock scope (what we prepare for); refine prompts and UI copy | Day 3–4 |
| **D. Five system prompts** | Implement 5 techniques; add way to compare (e.g. dropdown); document "best" | Day 4–6 |
| **E. Parameter tuning** | Expose ≥1 setting in UI; document effect on output | Day 6–7 |
| **F. Security** | Implement ≥1 guard; document in Reflection | Day 7–8 |
| **G. UI polish** | Clear labels, layout, error messages | Day 8–9 |
| **H. Documentation** | Fill "Understanding core concepts", "Technical implementation", "Reflection" below | Day 9–10 |
| **I. Optional + deploy** | Optional tasks (if any), GitHub repo, deploy (e.g. Streamlit Community Cloud), presentation prep | Day 10–14 |

### 1.5 Interview prep focus and approach (IT interviews)

**Strategy:** Satisfy minimal requirements first with one flexible flow, then add optional tasks (≥2 medium + 1 hard, more if time).

**Focus for MVP:** One mode that supports **multiple IT interview angles** via user input, not four separate features:

| Angle | How we support it in MVP |
|-------|---------------------------|
| **Behavioural** | User asks e.g. "Give me 5 behavioural questions for a senior role" or "STAR method practice". |
| **Technical** | User asks e.g. "Ruby on Rails technical interview questions" or "System design for a mid-level backend role". |
| **Questions to ask them** | User asks e.g. "What should I ask the interviewer at the end?" or "Questions to ask a CTO". |
| **Custom / job-specific** | User can paste a job description or role and ask "Prepare me for this" (optional task later: dedicated job-description field + RAG). |

So: **one text area (or short dropdown + text)** where the user describes what they want (e.g. "Behavioural", "Technical – Ruby", "Questions to ask", or free text). One "Generate" button. One system prompt that frames the assistant as an **IT interview coach** who can do all of the above depending on the user message. No need to build separate flows for MVP.

**Where to start (concrete):**

1. **Phase A** — Setup: `requirements.txt`, `.env.example`, minimal Streamlit page (title, one text input, one button, placeholder response).
2. **Phase B** — Single OpenAI call: one strong system prompt (e.g. "You are an IT interview coach. Help with behavioural questions, technical questions, and questions to ask the interviewer. Be concise and practical."), user message = what the user typed, show response in UI.
3. **Phase C** — Lock this focus in the UI: e.g. a dropdown "What do you want to practice?" (Behavioural / Technical / Questions to ask / Custom) that pre-fills or guides the user message; optional short tips. Refine system prompt if needed.
4. **Phases D–H** — Add 5 system prompts (different techniques), parameter tuning, security, polish, documentation.
5. **Phase I** — Optional: at least 2 medium (e.g. deploy + cost display, or job description field + JSON output) and 1 hard (e.g. full chatbot UI). Then add more optional tasks if time (personas, difficulty levels, all settings as sliders, etc.).

This keeps the MVP small, clearly "IT interview" focused, and leaves room to impress with optional tasks.

---

## 2. Understanding core concepts (study before presentation)

*To be filled during implementation. Use this to explain concepts clearly.*

### 2.1 Prompting techniques

We implemented five system prompts, one per technique (Phase D). The user can select which to use via a dropdown; the same request can be tried with different techniques to compare.

- **Zero-shot:** The model gets only instructions (no examples). We tell it it is an IT interview coach and what to help with; it follows the instructions directly. Good baseline and fast to iterate.
- **Few-shot:** The system prompt includes 1–2 short example exchanges (user request → coach response). The model mimics style and depth. Often gives more consistent, practical answers for interview prep.
- **Chain-of-thought (CoT):** We ask the model to structure its response in steps: e.g. (1) Analyze the request, (2) Plan what to provide, (3) Give the content, (4) Add a tip. Makes reasoning visible and can improve clarity.
- **Role / persona:** The system prompt defines a strong character (e.g. “You are a senior engineering manager who has run hundreds of interviews”). Output tends to feel more realistic and interviewer-like.
- **Structured output:** We require a fixed format (e.g. “## Questions”, “## What interviewers look for”, “## Sample answers”). Ensures consistent sections and makes it easy to scan.

*Which we used in Interview Lab:* All five, selectable in the UI. *Which worked best:* Try the same request with each; for interview prep, **Few-shot** and **Role (persona)** often give the most usable, concrete answers; **Structured output** is best when you want a consistent layout every time.

### 2.2 LLM settings and their effect on output

- **Temperature:** Controls randomness in the model’s choices. Range typically 0–2. Lower (e.g. 0.2–0.4): more deterministic, repetitive, “safe” wording. Higher (e.g. 0.8–1.0): more varied, creative, sometimes less focused. For Q&A and interview prep, 0.5–0.7 is a common sweet spot.
- **Top-p (nucleus sampling):** We don’t expose it in the UI yet; the API can use it alongside temperature. It limits choices to the smallest set of tokens whose cumulative probability exceeds p (e.g. 0.9), which can reduce irrelevant or off-topic tokens.
- **Frequency penalty / presence penalty:** We don’t use them in the app yet. They discourage repetition (frequency) or repeating topics (presence).
- *What we tuned in Interview Lab:* We expose **temperature** via a slider (0.0–1.0, default 0.7). Lower values give more consistent, textbook-style answers; higher values give more variety in examples and phrasing. The chosen value is shown next to each response so users can relate output to the setting.

### 2.3 User, system, and assistant roles

- **System:** …  
- **User:** …  
- **Assistant:** …  
- *How we use them in our API calls.*

### 2.4 LLM output types

- Plain text vs structured (e.g. JSON).  
- *What our app uses and why.*

---

## 3. Technical implementation

*To be filled during implementation. Describes how the project meets the evaluation criteria.*

### 3.1 How the app works (interview prep with ChatGPT)

- **User flow:** User chooses “What do you want to practice?” (Behavioural / Technical / Questions to ask them / Custom), enters their request in the text area, selects a “Prompt technique” (Zero-shot, Few-shot, Chain-of-thought, Role, Structured output), and clicks Generate. The app sends the chosen system prompt plus the user message to the OpenAI API and displays the model’s reply. The response is shown with the technique name so users can compare runs.
- **Where the “interview prep” value is:** The system prompts frame the model as an IT interview coach; the practice-type dropdown and user message (including category tag) steer content (behavioural vs technical vs questions to ask, etc.).

### 3.2 OpenAI API usage

- **Client:** We use the `openai` Python package: `OpenAI(api_key=api_key)` and `client.chat.completions.create(...)`.
- **Parameters sent:** `model="gpt-4o-mini"`; `messages` = list of dicts with `role` and `content` (one system message with the chosen prompt, one user message with the request); `temperature` = value from the UI slider (0.0–1.0, default 0.7).
- **System vs user:** The system message is the selected entry from `SYSTEM_PROMPTS[prompt_technique]`. The user message is `"[{practice_type}] {user_input}"` so the model knows the category and the exact request.

### 3.3 Front-end (Streamlit)

- **Main components used:** `st.selectbox` for practice type and for prompt technique; `st.slider` for temperature (Phase E); `st.text_area` for the user request; `st.button` for Generate; `st.spinner` while waiting; `st.success` and `st.markdown` for the reply; `st.caption` for tips; `st.error` / `st.warning` for validation and API errors.
- **State:** Streamlit reruns on each interaction; no `st.session_state` used for chat history (single request/response per run).
- **Where prompts and settings are configured:** System prompts are in `app.py` in the `SYSTEM_PROMPTS` dict (Phase D); the selected prompt is passed to the API. Temperature is set via the slider (Phase E) and passed to the API; model and other parameters are set in code.

### 3.4 Security guard(s)

- **What we implemented (Phase F):** One guard — **input length limit**. We cap the user request at **3000 characters** (`MAX_INPUT_LENGTH`). The text area uses `max_chars=3000` and we check length before calling the API. This limits prompt size, token cost, and abuse (e.g. pasting huge text).
- **How it prevents misuse:** The length cap bounds cost and keeps inputs to a reasonable size.

---

## 4. Reflection and improvement

*To be filled during/after implementation. Use this to justify choices and show awareness of limitations.*

### 4.1 Choice of prompt techniques and parameter settings

- Why we chose specific prompting techniques.  
- Why we chose specific parameter values (e.g. temperature).

### 4.2 Potential problems with the application

- **Limitations:** Cost scales with use (no per-user caps beyond input length). Quality depends on the model and prompt; the app does not verify facts. Single request/response per run (no chat history). Edge cases: very short or vague requests may get generic answers; long job descriptions may hit the 3000-character limit.
- **Risks:** **Prompt injection:** We do not yet validate or block override-style input. **Misuse:** Input length limits some abuse; we do not rate-limit or authenticate. API key in `.env` must stay server-side and never be committed.

### 4.3 Suggestions for improvement

- Code: …  
- Prompts: …  
- Product: …

---

*Last updated: Feb 17, 2025 — Project plan and structure. Content to be completed during implementation.*

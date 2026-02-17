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

- **Zero-shot:** …  
- **Few-shot:** …  
- **Chain-of-thought (CoT):** …  
- **Role / persona:** …  
- **Structured output:** …  
- *Which we used in Interview Lab and why.*

### 2.2 LLM settings and their effect on output

- **Temperature:** …  
- **Top-p:** …  
- **Frequency penalty / presence penalty:** …  
- *What we tuned and how it changed behaviour.*

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

- User flow: …  
- Where the "interview prep" value is (e.g. question types, feedback style).

### 3.2 OpenAI API usage

- Endpoint / client (e.g. `openai` Python package).  
- Parameters sent: model, messages (system/user/assistant), temperature, etc.  
- How we pass system vs user prompts.

### 3.3 Front-end (Streamlit)

- Main components used.  
- How state is handled (if any).  
- Where prompts and settings are configured.

### 3.4 Security guard(s)

- What we implemented.  
- How it prevents misuse.

---

## 4. Reflection and improvement

*To be filled during/after implementation. Use this to justify choices and show awareness of limitations.*

### 4.1 Choice of prompt techniques and parameter settings

- Why we chose specific prompting techniques.  
- Why we chose specific parameter values (e.g. temperature).

### 4.2 Potential problems with the application

- Limitations (e.g. cost, quality, edge cases).  
- Risks (e.g. prompt injection, misuse).

### 4.3 Suggestions for improvement

- Code: …  
- Prompts: …  
- Product: …

---

*Last updated: Feb 17, 2025 — Project plan and structure. Content to be completed during implementation.*

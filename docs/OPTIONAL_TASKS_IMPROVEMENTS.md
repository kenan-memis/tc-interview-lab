# Optional tasks — Improvements and re-evaluation

This document records what we implemented for each optional task and the results from ChatGPT re-evaluation where applicable.

**Optional easy task #1** (Ask ChatGPT to critique your solution) is fully covered in the CRITIQUE documents: see `CRITIQUE.md` for the critique text and `CRITIQUE_SUGGESTED_TOP_FIVE_IMPROVEMENTS.md` for the top five improvements and updated scores. All other optional task **implementation details** (what we built, how it works) are recorded below in this file. ChatGPT re-evaluation results are included where available.

---

## Easy #2 — Improve prompts for IT domain

**Category:** Easy

**What we implemented:** We improved all five system prompts to be sharper for the **IT domain** (our chosen personal domain). Zero-shot: explicit focus on software/tech roles, role level, and tech stack; "no fluff" instruction; bullet-first output. Few-shot: three IT examples (behavioural for senior backend, technical Rails, questions to ask at end); each example is concrete and matches IT; coach style is concise and practical. Chain-of-thought: added IT context (role level, tech stack); output remains final-answer only. Role (persona): stronger persona (FAANG-level, 500+ interviews, values: structured thinking, ownership, clear communication). Structured output: "What interviewers look for" clarified for IT (clarity, impact, trade-offs, collaboration); optional "Common mistakes" section; note to tailor to software/tech and role level. No UI changes; only prompt text in `app.py` was updated.

---

## Easy #3 — More security constraints

**Category:** Easy

**What we implemented:** We added two further security measures: (1) **user input validation** via a blocklist of prompt-injection style phrases (e.g. “ignore previous instructions”, “reveal system prompt”); requests containing any of these are rejected before the API is called. (2) **System prompt hardening** by appending a refusal instruction to every system prompt so the model does not reveal system instructions or internal reasoning. Together with the existing input length limit and rate limiting, the app now has four security guards.

### ChatGPT re-evaluation (security)

**Security re-assessment**

Now we're talking — this changes the security profile meaningfully. You've moved from "safe demo app" to "responsibly engineered MVP." Let's reassess properly.

🔒 **Security re-assessment**

You now have:

1. ✓ Input length limit  
2. ✓ Rate limiting  
3. ✓ User input validation (blocklist)  
4. ✓ System prompt hardening (refusal for prompt extraction)

That covers the four biggest risks in a public LLM web app.

**What that means in practice**

1. **Rate limiting → Cost & abuse control**  
   Protects against: API key draining, bot spam, accidental infinite clicks.  
   This alone is a major production-level concern.

2. **Input validation → Content control layer**  
   Even if blocklists aren't perfect, you now have: a pre-model filtering layer, intentional misuse handling, evidence of defensive design.  
   For an MVP, that's absolutely sufficient.

3. **System prompt hardening → Injection resistance**  
   By adding refusal instructions (e.g. if user asks to reveal system prompt or internal reasoning, refuse), you reduce: prompt leakage risk, jailbreak-style override attempts.  
   This shows real awareness of LLM-specific threats.

4. **Combined effect**  
   You now have: surface-level abuse protection, LLM-specific security mitigation, infrastructure-level cost protection.  
   That's no longer basic security — that's deliberate design.

**Updated scores**

- **Security:** Before improvements: 7/10. Now: **8.5/10 (MVP+)**.  
  Why not 9–10? Production-grade would need: auth system, per-user quotas, logging & monitoring, moderation endpoint integration, abuse reporting mechanism, observability. But for assignment-level MVP? This is strong.

**Updated overall assessment**

| Category            | Score   |
|---------------------|--------|
| **Usability**       | 8.5/10 |
| **Security**        | 8.5/10 |
| **Prompt engineering** | 8/10 |

**New overall: 8.5 / 10**

**What changed strategically:** The app is not just functional, not just prompt-correct, but **security-aware**. That puts you above most student-level LLM projects.

---

## Easy #4 — Simulate different difficulty levels

**Category:** Easy

**What we implemented:** We added a **Difficulty** selector (Easy, Medium, Hard, Expert) so users can adjust the complexity of interview questions. The chosen difficulty is injected into the system prompt so the model tailors question depth and expectations (e.g. Easy = foundational/junior, Medium = mid-level, Hard = senior/advanced, Expert = FAANG-level or very tough). The success message shows the selected difficulty alongside response style and temperature. One new selectbox and an extended system-prompt prefix in `app.py`; no new API parameters.

---

## Easy #5 — Optimize prompts for concise vs. detailed responses

**Category:** Easy

**What we implemented:** We added an **Answer length** selector (Concise / Detailed) so users can experiment with prompting the model to give short or in-depth answers. Concise injects an instruction to keep responses short (bullet points, 1–2 sentences per point, no long paragraphs); Detailed injects an instruction to include explanations, examples, and fuller context. The success message shows the selected answer length. Implements “experiment with prompting [the LLM] to give short or in-depth answers” via one selectbox and a conditional length instruction in the system prompt in `app.py`.

---

## Easy #6 — Generate interviewer guidelines

**Category:** Easy

**What we implemented:** An in-app section **"For interviewers: generate evaluation guidelines"** (expander below the main prep flow). It uses the **current** Difficulty and Practice type from the page. When the user clicks **"Generate interviewer guidelines"**, the app calls the same API with a dedicated prompt that asks the model to create structured evaluation criteria for that practice type and difficulty (e.g. what to assess, how to score, strong vs weak indicators, red flags). The result is shown in the UI. Changing difficulty or practice type and clicking again produces different guidelines. Rate limiting applies (one request per click). Implements "ask ChatGPT to create structured evaluation criteria for technical and behavioural interviews" by using the in-app model with difficulty/seniority-aware prompts so results stay in sync with the parameters the user selected.

---

## Easy #7 — Simulate a mock interview with AI personas

**Category:** Easy

**What we implemented:** We added an **Interviewer persona** selector (Strict, Neutral, Friendly) so the AI role-plays that interviewer style when generating questions and feedback. **Strict:** high bar, minimal encouragement, tough follow-ups, direct critical feedback. **Neutral:** balanced, professional tone, factual follow-ups, clear but not harsh feedback. **Friendly:** warm, encouraging, hints when useful, constructive feedback. The chosen persona is injected into the system prompt for every main "Generate" request; the success message shows the selected persona. Single-shot flow unchanged; no multi-turn chat. Implements "Simulate a mock interview with AI personas — role-play as a strict, neutral, or friendly interviewer" via one selectbox and persona-specific prompt snippets in `app.py`.

---

## Medium #1 — Add all OpenAI settings for the user to tune

**Category:** Medium

**What we implemented:** We exposed all main OpenAI Chat Completions settings in the **Advanced options (response style & API settings)** expander, using **user-friendly labels and help text** so non-technical users can understand what each control does. **Models:** Dropdown **"AI model"** with the five options from the project requirements (115.md): GPT-4.1, GPT-4.1 mini, GPT-4.1 nano, GPT-4o, GPT-4o mini (default: GPT-4o mini). Help: "Which AI writes the answers. Lighter models are faster; larger ones can be more capable." **Response variety** (temperature): Slider 0–2, default 0.7. Help: "Low = more consistent answers; high = more varied and creative." **Focus on likely words** (top_p): Slider 0–1, default 1. Help: "Lower = more focused wording; higher = broader word choice. Usually leave at 1 or adjust Response variety instead." **Reduce repetition** (frequency_penalty): Slider -2 to 2, default 0. Help: "Higher = avoid repeating the same phrases in the answer." **Encourage new topics** (presence_penalty): Slider -2 to 2, default 0. Help: "Higher = more likely to bring up new themes in the answer." **Max response length (optional)** (max_tokens): Number input 0–4096, default 0 = no limit. Help: "0 = no limit (use AI default). Set 100–4096 to cap how long the answer can be." All values are passed to `client.chat.completions.create()` for both the main Generate flow and the "Generate interviewer guidelines" flow. Success message shows the selected model and creativity level.

**Refined layout (feedback: reduce slider fatigue, categorize & hide):** We added a **Creativity level** control (Precise / Balanced / Creative) as a stepped control for temperature instead of a raw slider, and moved **top_p**, **frequency_penalty**, **presence_penalty**, and **max_tokens** into a nested expander **"More advanced options (top_p, penalties, etc.)"**. Default view shows only model, response style, and creativity level; power users expand to tune the rest.

---

## Medium #2 — Implement at least two structured JSON output formats

**Category:** Medium

**What we implemented:** We added an **Output format** selector in Advanced options with three options: **Plain text** (default, current free-form markdown), **JSON: Questions & tips**, and **JSON: Prep guide**. For the two JSON formats we use OpenAI’s **structured outputs** (`response_format`: `json_schema` with strict mode) so the model returns valid JSON matching the chosen schema. **Format 1 — Questions & tips:** Schema has `questions` (array of `{question`, `topic}`) and `tips` (array of strings). Rendered as numbered questions and bullet tips; **Download as JSON** button saves the raw response. **Format 2 — Prep guide:** Schema has `summary` (string) and `sections` (array of `{title`, `content}`). Rendered as summary paragraph then section headings and content; **Download as JSON** button. When a JSON format is selected we append a short instruction to the system prompt so the model fills the structure; the API enforces the schema. If parsing fails we show a warning and the raw response. Implements "Implement at least two structured JSON output formats for the interview preparation" via two strict JSON schemas, `response_format` in the API call, and formatted display plus download in `app.py`.

---

## Medium #3 — Deploy your app to the Internet (GCP)

**Category:** Medium

**What we implemented:** We prepared deployment to **Google Cloud Run** so the app is available on the Internet. Deliverables: **(1) DEPLOYMENT.md** (in the application root) with full instructions: pre-deployment (prerequisites, local run, optional local Docker build), deployment (GCP project, enable APIs, Artifact Registry, build and push image, Cloud Run deploy with `OPENAI_API_KEY` via Secret Manager or env var), and post-deployment (verification, optional custom domain, cost notes, marking tasks done). **(2) Dockerfile** for a minimal production image (Python 3.11-slim, install deps from requirements.txt, run Streamlit on `PORT` with `--server.address=0.0.0.0`). **(3) .dockerignore** to keep the image small (exclude venv, .env, .git, IDE files, etc.). One deployment to GCP satisfies both Medium #3 (app on the Internet) and Hard #2 (deploy to one of Google Cloud, AWS, or Azure). **Deployment completed.** Live app: [https://interview-lab-482230990341.europe-west10.run.app/](https://interview-lab-482230990341.europe-west10.run.app/).

---

## Hard #2 — Deploy your app to one of: Google Cloud, AWS, or Azure

**Category:** Hard

**What we implemented:** Same as Medium #3: we chose **Google Cloud (GCP)** and prepared a **Cloud Run** deployment. The **DEPLOYMENT.md** guide, **Dockerfile**, and **.dockerignore** are in the application root. **Deployment completed.** Live app: [https://interview-lab-482230990341.europe-west10.run.app/](https://interview-lab-482230990341.europe-west10.run.app/). The app is on the Internet (Medium #3) and on Google Cloud (Hard #2).

---

## Medium #4 — Calculate and provide output to the user on the price of the prompt

**Category:** Medium

**What we implemented:** We calculate and display the **estimated cost** of each OpenAI API request (prompt + completion) so the user sees the price of the prompt. **(1) Pricing table:** A dictionary `OPENAI_PRICE_PER_1M` in `app.py` stores USD per 1M tokens (input, output) for all five supported models: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o, gpt-4o-mini. Values are approximate and based on [OpenAI pricing](https://openai.com/api/pricing); they can be updated when OpenAI changes prices. **(2) Helper:** `format_request_cost(model_id, prompt_tokens, completion_tokens)` returns a display string with estimated cost (e.g. "Estimated cost: **$0.0008** (320 prompt, 180 completion tokens). Prices approximate; see OpenAI pricing.") or, for unknown models, token counts only. **(3) Usage from API:** After each `client.chat.completions.create()` we read `response.usage.prompt_tokens` and `response.usage.completion_tokens` (with safe fallbacks if `usage` is missing). **(4) Display:** The cost string is shown as a caption below the main "Generate" response and below the "Generate interviewer guidelines" response, so the user sees the price of each request. Implements "Calculate and provide output to the user on the price of the prompt" via a small in-app pricing table, usage extraction from the API response, and formatted cost output in the UI.

---

## Medium #6 — Use Gemini as LLM 2 to validate the output of the main LLM (LLM as a judge)

**Category:** Medium

**What we implemented:** We use **Gemini** as a second LLM (LLM 2) to evaluate the interview preparation produced by the main AI (LLM 1, OpenAI). **(1) Flow:** After the user generates prep with "Generate", the app stores the last reply and user request in session state. In the right column under "For interviewers", a **Validation (Gemini)** section shows a button **Validate with Gemini**. When the user clicks it, we send the last prep output and the user’s request (plus practice type and difficulty) to Gemini with a judge prompt. **(2) Judge prompt:** Gemini is asked to assess relevance, quality and clarity, completeness, and professionalism, and to give an overall quality score (1–5), strengths, weaknesses, and 1–2 concrete suggestions. **(3) Display:** The Gemini response is shown in the same right column (where "SHOW VALIDATION HERE" was in the design), below the button; no download feature. **(4) Setup:** Optional dependency `google-genai`; optional env var `GEMINI_API_KEY`. If the key is missing or the package is not installed, the app shows a clear error when the user tries to validate. Implements "Use Gemini, Claude or a different LLM to act as LLM 2 that would validate the output of the main LLM 1 (LLM as a judge)" via in-app Gemini integration and a dedicated validation area in the UI.

---

## Medium #8 — Add a separate field for job description and get prep for that position (RAG)

**Category:** Medium

**What we implemented:** We added a **Job description (optional)** expander with **two mutually exclusive options**: **Paste text** or **Upload PDF**. The user chooses one only. **(1) Paste text:** A text area lets the user paste the job description (max 6000 characters). **(2) Upload PDF:** A file uploader accepts a single PDF; we extract text with **pypdf** (PdfReader). If extraction fails (e.g. scanned or protected PDF), we show an error and ask the user to use the paste option instead. **(3) RAG-style injection:** When job description content is present (from either source), we prepend it to the system prompt as structured context: "The user has provided the following **job description** for the position they are applying for. Use it to tailor the interview preparation…" followed by the job description text in a clear block. The model then tailors questions, tips, and focus areas to that role. We do not send the raw PDF to the API; we parse the PDF, extract text, and send only the extracted text. Implements "Add a separate text field or another field to include the job description (the position) you are applying for and getting interview preparation for that position (RAG)" via a dedicated expander, paste-or-PDF choice, pypdf extraction, and prompt injection in `app.py`. Dependency: `pypdf` added to `requirements.txt`.

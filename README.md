# Interview Lab

A single-page web application for interview preparation, powered by the OpenAI API and prompt engineering. Built with Python and Streamlit for the Turing College AI Engineering course (Sprint 1).

---

## What it is for

Interview Lab helps you prepare for job interviews by:

- Practising behavioural questions, technical questions (e.g. Ruby/Rails), "questions to ask the interviewer", or custom prep (e.g. pasting a job description).
- Interacting with a ChatGPT-style assistant that acts as an IT interview coach.
- Experimenting with different prompt styles and model settings to see what works best for your use case.

---

## How it is built

- **Language:** Python  
- **UI:** Streamlit (single-page app; no separate front-end stack).  
- **LLM:** OpenAI API (we use **GPT-4o mini**).  
- **Main techniques:** System and user prompts, multiple prompting strategies (e.g. zero-shot, few-shot, chain-of-thought), and at least one tuned parameter (e.g. temperature).  
- **Security:** At least one guard against misuse (e.g. input validation, length limits).  

For evaluation-focused details (prompting techniques, settings, roles, reflection), see **docs/PROJECT_PLANNING_AND_EVALUATION.md**.

---

## How to run it

Anyone who wants to try the app can follow these steps. You need Python, an OpenAI API key, and a terminal.

### Prerequisites

- **Python 3.10+** (recommended).
- **OpenAI API key** — create one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/interview-lab.git
cd interview-lab
```

*(Replace the URL with the actual repo URL if different.)*

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your OpenAI API key

- Copy the example env file and add your key:

```bash
cp .env.example .env
```

- Open `.env` and set your key (do not commit this file — it is in `.gitignore`):

```
OPENAI_API_KEY=sk-your-key-here
```

### 5. Run the app

From the project root (`interview-lab/`), run:

```bash
streamlit run app.py
```

- Open the URL shown in the terminal (usually **http://localhost:8501**) in your browser.
- You should see the Interview Lab page: choose what to practice, enter your request, optionally open "Advanced options" for prompt technique and temperature, then click **Generate** to get interview prep from the model.

---

## Deployment

**Live app (production):** [https://interview-lab-482230990341.europe-west10.run.app/](https://interview-lab-482230990341.europe-west10.run.app/)

To deploy the app to **Google Cloud Run** (and satisfy the course optional tasks for “deploy to the Internet” and “deploy to GCP”), see **[DEPLOYMENT.md](DEPLOYMENT.md)**. It covers pre-deployment checks, building the Docker image, pushing to Artifact Registry, deploying to Cloud Run, and setting the `OPENAI_API_KEY` secret. The repo includes a **Dockerfile** and **.dockerignore** for a minimal production image.

---

## Project structure

```
interview-lab/
├── README.md           # This file — what the app is, how to run
├── DEPLOYMENT.md       # Deployment to Google Cloud Run (pre-, deploy, post-steps)
├── Dockerfile          # Production image for Cloud Run
├── docs/               # Documentation (no README here)
│   ├── PROJECT_PLANNING_AND_EVALUATION.md   # Project plan, core concepts, technical implementation, reflection
│   ├── OPTIONAL_TASKS.md   # Checklist of optional tasks (easy/medium/hard); mark [x] when done
│   ├── CRITIQUE.md         # ChatGPT critique (usability, security, prompt-engineering)
│   ├── CRITIQUE_SUGGESTED_TOP_FIVE_IMPROVEMENTS.md
│   └── ...
├── requirements.txt    # Python dependencies
├── .env.example        # Example env vars (no secrets)
├── app.py                      # Streamlit entry point (or main module)
├── jailbreak_experiment_results.csv   # Medium #7: jailbreak test results (invalid prompt, message, job file)
└── ...
```

---

## Optional tasks

Checklist of all optional tasks (easy, medium, hard). Mark with `[x]` when implemented.  
*For maximum bonus points: implement at least 2 medium and 1 hard (or 2 medium + 2 hard — confirm with your course materials).*

### Easy

- [x] **1.** Ask ChatGPT to critique your solution from the usability, security, and prompt-engineering sides.
- [x] **2.** Improve ChatGPT prompts for your personal domain (IT, finance, HR, communication, etc.).
- [x] **3.** Implement more security constraints (e.g. user input validation, system prompt validation). Consider using ChatGPT to verify these aspects.
- [x] **4.** Simulate different difficulty levels — adjust the complexity of interview questions (easy, medium, hard).
- [x] **5.** Optimize prompts for concise vs. detailed responses — experiment with short or in-depth answers.
- [x] **6.** Generate interviewer guidelines — ask ChatGPT to create structured evaluation criteria for technical and behavioural interviews.
- [x] **7.** Simulate a mock interview with AI personas — role-play as a strict, neutral, or friendly interviewer.

### Medium

- [x] **1.** Add all OpenAI settings (model, temperature, frequency, etc.) for the user to tune as sliders/fields.
- [x] **2.** Implement at least two structured JSON output formats for the interview preparation.
- [x] **3.** Deploy your app to the Internet.
- [x] **4.** Calculate and provide output to the user on the price of the prompt.
- [ ] **5.** Read OpenAI API documentation, think of your own improvement, and implement it.
- [x] **6.** Use Gemini, Claude or another LLM as LLM 2 to validate the output of the main LLM (LLM as a judge).
- [x] **7.** Try to jailbreak your own application (invalid prompt, message, job file, etc.). Document results in an Excel sheet.
- [x] **8.** Add a separate text field for the job description and get interview preparation for that position (RAG).
- [ ] **9.** Let the user choose from a list of LLMs (Gemini, OpenAI, etc.).
- [ ] **10.** Think of a creative way to use image generation in this project and implement it.

### Hard

- [ ] **1.** Implement a full-fledged chatbot (multi-turn) instead of a one-time call — Streamlit or React.
- [x] **2.** Deploy your app to one of: Google Cloud (Gemini), AWS, or Azure.
- [ ] **3.** Use LangChain (chains or agents) to implement the app.
- [ ] **4.** Add a vector database to check if interview preparation data was seen before; prompt LLM to generate new content when needed.
- [ ] **5.** Use open-source LLMs (not Gemini, OpenAI, etc.) for the project.
- [ ] **6.** Assess the performance of your prompt and/or model (e.g. LLM-as-a-judge or other methods).

*When you implement a task, change `- [ ]` to `- [x]` for that line. Update the "Optional tasks we implemented" section in evaluation_criteria.md (sprint_1) for your presentation.*

---

## License and course context

This project is part of the Turing College AI Engineering course, Sprint 1. It is for learning and portfolio purposes.

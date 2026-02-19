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

For evaluation-focused details (prompting techniques, settings, roles, reflection), see **docs/DOCUMENTATION.md**.

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
│   ├── DOCUMENTATION.md    # Core concepts, technical implementation, reflection
│   ├── OPTIONAL_TASKS.md   # Checklist of optional tasks (easy/medium/hard); mark [x] when done
│   ├── CRITIQUE.md         # ChatGPT critique (usability, security, prompt-engineering)
│   ├── CRITIQUE_SUGGESTED_TOP_FIVE_IMPROVEMENTS.md
│   └── ...
├── requirements.txt    # Python dependencies
├── .env.example        # Example env vars (no secrets)
├── app.py              # Streamlit entry point (or main module)
└── ...
```

---

## License and course context

This project is part of the Turing College AI Engineering course, Sprint 1. It is for learning and portfolio purposes.

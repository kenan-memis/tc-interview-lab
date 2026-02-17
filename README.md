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
- **LLM:** OpenAI API (model to be chosen: GPT-4.1, GPT-4.1 mini, GPT-4.1 nano, GPT-4o, or GPT-4o mini).  
- **Main techniques:** System and user prompts, multiple prompting strategies (e.g. zero-shot, few-shot, chain-of-thought), and at least one tuned parameter (e.g. temperature).  
- **Security:** At least one guard against misuse (e.g. input validation, length limits).  

For evaluation-focused details (prompting techniques, settings, roles, reflection), see **DOCUMENTATION.md**.

---

## How to run it

### Prerequisites

- Python 3.10+ (recommended).  
- An [OpenAI API key](https://platform.openai.com/api-keys).

### Setup

1. **Clone the repository** (once it exists):

   ```bash
   git clone <repository-url>
   cd interview-lab
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the API key:**

   - Copy `.env.example` to `.env`.  
   - Set your OpenAI API key in `.env` (do not commit `.env`).

   ```bash
   cp .env.example .env
   # Edit .env and set OPENAI_API_KEY=sk-...
   ```

### Run the app

From the project folder (`interview-lab/`), run:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`) in your browser. You should see the title, text area, and **Generate** button; clicking **Generate** shows the response (or placeholder until the API is connected).

---

## Project structure (to be updated)

```
interview-lab/
├── README.md           # This file — what the app is, how to run
├── DOCUMENTATION.md    # Core concepts, technical implementation, reflection
├── requirements.txt    # Python dependencies
├── .env.example        # Example env vars (no secrets)
├── app.py              # Streamlit entry point (or main module)
└── ...
```

---

## License and course context

This project is part of the Turing College AI Engineering course, Sprint 1. It is for learning and portfolio purposes.

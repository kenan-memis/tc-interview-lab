# Interview Lab — Deployment to Google Cloud (GCP)

This guide covers deploying the Interview Lab Streamlit app to **Google Cloud Run**. One deployment satisfies:

- **Medium optional task #3:** Deploy your app to the Internet.
- **Hard optional task #2:** Deploy your app to one of: Google Cloud (Gemini), AWS, or Azure.

---

## Table of contents

1. [Overview](#overview)
2. [Pre-deployment](#pre-deployment)
3. [Deployment](#deployment)
4. [Post-deployment](#post-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Overview

| Item | Detail |
|------|--------|
| **Target** | Google Cloud Run (serverless containers) |
| **App** | Streamlit app (`app.py`), single container |
| **Secrets** | `OPENAI_API_KEY` (required at runtime) |
| **Result** | A public HTTPS URL (e.g. `https://interview-lab-xxxxx.run.app`) |
| **Live app** | [https://interview-lab-482230990341.europe-west10.run.app/](https://interview-lab-482230990341.europe-west10.run.app/) |
| **Region** | This guide uses **europe-west10**. Use the same region for Artifact Registry and Cloud Run. |

You will:

1. Build a Docker image of the app.
2. Push the image to **Google Artifact Registry**.
3. Deploy the image to **Cloud Run** and provide the API key as a secret/environment variable.

---

## Pre-deployment

### 1. Prerequisites

- **Google Cloud account** — [console.cloud.google.com](https://console.cloud.google.com).
- **Billing** — Cloud Run and Artifact Registry require a billing account (there is a free tier; see [Cloud Run pricing](https://cloud.google.com/run/pricing)).
- **Local tools (choose one of the following):**
  - **Option A (recommended):** [Google Cloud CLI (`gcloud`)](https://cloud.google.com/sdk/docs/install) installed and initialized (`gcloud init`), and [Docker](https://docs.docker.com/get-docker/) installed (for building the image locally and pushing to Artifact Registry).
  - **Option B:** Only `gcloud` installed; you will use **Cloud Build** to build the image in the cloud (no local Docker required).

### 2. Verify the app runs locally

From the **application root** (`interview-lab/`):

```bash
# Create and activate a virtual environment (if not already)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key (copy .env.example to .env and set OPENAI_API_KEY)
# Then run the app
streamlit run app.py
```

Open `http://localhost:8501`, confirm the app loads and that a test request (e.g. Generate) works. This ensures the app and API key are correct before deployment.

### 3. (Optional) Build and run the Docker image locally

If you use Docker locally, you can confirm the container runs before pushing to GCP:

```bash
# From interview-lab/
docker build -t interview-lab:local .

# Run; pass your API key and map port 8080
docker run --rm -e OPENAI_API_KEY=sk-your-key-here -p 8080:8080 interview-lab:local
```

Open `http://localhost:8080`. If the app works, the same image is ready for Cloud Run.

---

## Deployment

### Step 1: Create or select a GCP project

1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Create a new project (e.g. `interview-lab-prod`) or select an existing one.
3. Note the **Project ID** (e.g. `interview-lab-prod`). You will use it in the next steps.

Set the project for the rest of the session:

```bash
gcloud config set project YOUR_PROJECT_ID
```

### Step 2: Enable required APIs

Enable **Cloud Run**, **Artifact Registry**, and (if you use Cloud Build) **Cloud Build**:

```bash
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 3: Create an Artifact Registry repository

This repository will store your Docker images.

```bash
# Create a Docker repository in region europe-west10 (use same region for repo and Cloud Run)
gcloud artifacts repositories create interview-lab-repo \
  --repository-format=docker \
  --location=europe-west10 \
  --description="Interview Lab Docker images"
```

If the repository already exists, skip this step.

### Step 4: Build and push the Docker image

**Option A — Build locally with Docker and push**

Configure Docker to use `gcloud` as a credential helper for Artifact Registry (use the **same region** as your repository):

```bash
gcloud auth configure-docker europe-west10-docker.pkg.dev
```

From the **application root** (`interview-lab/`), build and tag the image (replace `YOUR_PROJECT_ID` with your GCP project ID). **Use `--platform linux/amd64`** so the image runs on Cloud Run (which uses amd64/linux; without this, images built on Apple Silicon are arm64 and will fail to deploy):

```bash
docker build --platform linux/amd64 -t europe-west10-docker.pkg.dev/YOUR_PROJECT_ID/interview-lab-repo/interview-lab:latest .
docker push europe-west10-docker.pkg.dev/YOUR_PROJECT_ID/interview-lab-repo/interview-lab:latest
```

**Option B — Build in the cloud with Cloud Build (no local Docker)**

From the **application root** (`interview-lab/`), run (replace `YOUR_PROJECT_ID` with your GCP project ID):

```bash
gcloud builds submit --tag europe-west10-docker.pkg.dev/YOUR_PROJECT_ID/interview-lab-repo/interview-lab:latest .
```

This uploads the build context (respecting `.dockerignore`) and builds the image in GCP, then pushes it to Artifact Registry.

### Step 5: Deploy to Cloud Run

Deploy the image to Cloud Run and set the `OPENAI_API_KEY` secret. You can store the key in **Secret Manager** (recommended) or pass it as a plain environment variable (simpler but less secure).

**5a. Store the API key in Secret Manager (recommended)**

```bash
# Create the secret (you will be prompted to enter the secret value)
echo -n "sk-your-openai-api-key-here" | gcloud secrets create openai-api-key --data-file=-

# Grant Cloud Run access to the secret
gcloud secrets add-iam-policy-binding openai-api-key \
  --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

To find your project number: `gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)'`.

Then deploy, referencing the secret (replace `YOUR_PROJECT_ID` with your GCP project ID):

```bash
gcloud run deploy interview-lab \
  --image europe-west10-docker.pkg.dev/YOUR_PROJECT_ID/interview-lab-repo/interview-lab:latest \
  --region europe-west10 \
  --platform managed \
  --allow-unauthenticated \
  --set-secrets="OPENAI_API_KEY=openai-api-key:latest"
```

**5b. Or set the API key as an environment variable (simpler, less secure)**

```bash
gcloud run deploy interview-lab \
  --image europe-west10-docker.pkg.dev/YOUR_PROJECT_ID/interview-lab-repo/interview-lab:latest \
  --region europe-west10 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="OPENAI_API_KEY=sk-your-openai-api-key-here"
```

- `--allow-unauthenticated` makes the service publicly reachable (required for “deploy to the Internet”).
- Replace `YOUR_PROJECT_ID` with your GCP project ID. Use the same region as your Artifact Registry repository.

### Step 6: Get the service URL

After deployment, the CLI prints the **Service URL**. You can also fetch it with:

```bash
gcloud run services describe interview-lab --region europe-west10 --format='value(status.url)'
```

Open this URL in a browser to use the deployed app.

---

## Post-deployment

### 1. Verify the deployment

- Open the Cloud Run service URL in a browser.
- Confirm the Interview Lab UI loads.
- Run a short test (e.g. choose practice type, enter a request, click Generate).
- If the response is correct, the app and `OPENAI_API_KEY` are working.

### 2. Optional: custom domain and HTTPS

Cloud Run provides HTTPS by default on the `*.run.app` URL. To use a custom domain, follow [Google’s guide](https://cloud.google.com/run/docs/mapping-custom-domains).

### 3. Cost and quotas

- **Cloud Run** charges for CPU/memory and request count; there is a [free tier](https://cloud.google.com/run/pricing#free-tier).
- **Artifact Registry** has a [free storage tier](https://cloud.google.com/artifact-registry/pricing).
- Set budget alerts in the GCP Console if you want to avoid surprises.

### 4. Mark optional tasks complete

After a successful deployment:

- In **OPTIONAL_TASKS.md**, mark as done:
  - Medium #3: Deploy your app to the Internet.
  - Hard #2: Deploy your app to one of: Google Cloud (Gemini), AWS, or Azure.
- In **evaluation_criteria.md**, add the deployment URL and note that both tasks are satisfied by this GCP deployment.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| **App returns 500 or “Something went wrong”** | Ensure `OPENAI_API_KEY` is set correctly (Secret Manager or env var) and that the key is valid and has quota. |
| **“Permission denied” when pushing image** | Run `gcloud auth configure-docker europe-west10-docker.pkg.dev` (use the same region as your registry) and `gcloud auth login`. |
| **Cloud Run service not found** | Confirm region (`--region europe-west10`) matches where you deployed. |
| **Container fails to start** | Check Cloud Run logs in the console (Logging → Cloud Run service). Ensure the Dockerfile `CMD` uses `PORT` (Cloud Run sets it automatically). |
| **Streamlit shows “Please wait…” or blank** | Ensure the app listens on `0.0.0.0` (the Dockerfile uses `--server.address=0.0.0.0`). |

For more help, see [Cloud Run documentation](https://cloud.google.com/run/docs) and [Streamlit in Docker](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker).

# Interview Lab — Docker image for Google Cloud Run
# Python 3.13 slim to match local (3.13.x); keeps image size small
FROM python:3.13-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and entrypoint (app does not require docs/ at runtime)
COPY app.py .
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Cloud Run sets PORT (default 8080); Streamlit must listen on 0.0.0.0
ENV STREAMLIT_SERVER_PORT=8080
EXPOSE 8080

# JSON form for CMD so the process receives OS signals (e.g. SIGTERM) correctly
ENTRYPOINT ["/docker-entrypoint.sh"]

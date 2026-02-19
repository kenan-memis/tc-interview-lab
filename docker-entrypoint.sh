#!/bin/sh
# Use PORT from environment (Cloud Run sets it); exec so Streamlit gets OS signals (e.g. SIGTERM)
exec streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0 --server.headless=true

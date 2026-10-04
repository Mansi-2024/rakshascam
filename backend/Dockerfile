# Production Dockerfile for RakshaScan FastAPI Backend
# SANGYAN 2026 Hackathon | Track A: Digital Fraud & Scam Resilience

FROM python:3.14-slim

# Set environment variables for production execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    PORT=8000

# Install system dependencies required for offline local Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Set working directory to /app so `app.main:app` resolves cleanly
WORKDIR /app

# Install dependencies first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application source
COPY app/ ./app/

# Expose default port (overridden dynamically by Render runtime via $PORT)
EXPOSE 8000

# Launch Uvicorn production server binding to 0.0.0.0 and dynamically resolving $PORT
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

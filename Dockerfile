# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# --- FIX: Update system packages and install required SSL libraries ---
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        libssl-dev \
        # Add ca-certificates to ensure SSL certificates are up-to-date
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Update CA certificates
    && update-ca-certificates --fresh
# --------------------------------------------------------------------

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY ./app /app/app

# Expose port 8000 (or use the PORT environment variable)
EXPOSE 8000

# Use the PORT environment variable dynamically
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
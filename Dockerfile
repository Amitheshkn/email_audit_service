# --- Base image ---
FROM python:3.10-slim as base

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /email_audit_service

# --- Build stage ---
FROM base as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Final image ---
FROM base as final

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . /email_audit_service

# Set PYTHONPATH so modules are discoverable
ENV PYTHONPATH=/email_audit_service:$PYTHONPATH

# Expose the Flask port (default 5000)
EXPOSE 8000

# Set entrypoint
CMD ["python", "bin/email_audit_app"]

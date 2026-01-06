FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --upgrade pip \
    && pip install .

# Copy application code
COPY app ./app
COPY migrations ./migrations

# Worker runs a Python module, not HTTP
CMD ["python", "-m", "app.workers.consumer"]

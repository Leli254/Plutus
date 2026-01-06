FROM python:3.12-slim

# Prevent Python from writing pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Working directory inside container
WORKDIR /app

# Install Python dependencies first (layer caching)
COPY pyproject.toml .
RUN pip install --upgrade pip \
    && pip install .

# Copy application code
COPY app ./app
COPY migrations ./migrations

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

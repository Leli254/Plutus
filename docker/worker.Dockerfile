FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy poetry files and install dependencies
COPY pyproject.toml poetry.lock* ./

RUN pip install --upgrade pip \
    && pip install poetry poetry-plugin-export

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt \
    && pip install -r requirements.txt \
    && rm requirements.txt

# Copy application code
COPY . .

# Copy entrypoint script
COPY docker/worker-entrypoint.sh ./docker/worker-entrypoint.sh
RUN chmod +x ./docker/worker-entrypoint.sh

# Use entrypoint to wait for DB and run worker
ENTRYPOINT ["sh", "./docker/worker-entrypoint.sh"]
CMD ["python", "-m", "workers.consumer"]
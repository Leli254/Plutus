FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definitions only
COPY pyproject.toml poetry.lock* ./

# Install Poetry + export plugin
RUN pip install --upgrade pip \
    && pip install poetry poetry-plugin-export

# Export dependencies and install via pip
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt \
    && pip install -r requirements.txt \
    && rm requirements.txt

# Copy application code (root-level main.py preserved)
COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
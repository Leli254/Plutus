# Plutus

A scalable, idempotent, async event ingestion and processing system built with FastAPI, async SQLAlchemy, and background workers.

This project demonstrates mid-to-senior level Python backend engineering patterns, including:

Idempotent ingestion

Async database access

Background processing

Observability (metrics + tracing)

Clean architecture & separation of concerns

Dockerized deployment

High-Level Architecture
Clients / Webhooks
        |
        v
   FastAPI API
        |
        v
   RawEvent (DB)
        |
        v
 Background Worker
        |
        +--> ProcessedEvent (success)
        |
        +--> FailedEvent (failure)

Key Features
Ingestion

Accepts webhook-style events

Enforces idempotency using a database constraint

Stores immutable raw payloads

Returns a stable event ID

Processing

Background worker polls pending events

Normalizes payloads into a canonical format

Persists processed results

Handles failures with retry-friendly state tracking

Observability

Prometheus metrics for:

Ingestion counts

Processing success/failure

Worker activity

OpenTelemetry tracing across:

API requests

Ingestion

Processing

Worker execution

Engineering Quality

Async-first (FastAPI + SQLAlchemy async)

Clear domain boundaries

Structured logging

Docker-based runtime parity

Repository Structure
ingestor/
├── app/
│   ├── api/                  # FastAPI routers
│   │   └── v1/
│   ├── core/                 # App wiring & infrastructure
│   ├── db/                   # Database layer
│   ├── ingestion/            # Ingress use-cases
│   ├── processing/           # Business logic
│   ├── workers/              # Background workers
│   ├── observability/        # Metrics & tracing
│   ├── main.py               # FastAPI entrypoint
│   └── __init__.py
│
├── migrations/               # Alembic migrations
├── tests/
│   ├── unit/
│   └── integration/
│
├── docker/
│   ├── api.Dockerfile
│   └── worker.Dockerfile
│
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── .gitignore

Technology Stack

Python 3.12

FastAPI

SQLAlchemy (async)

PostgreSQL

Prometheus

OpenTelemetry

Docker & Docker Compose

Environment Variables

Create a .env file (or use environment injection):

DATABASE_URL=postgresql+asyncpg://user:password@db:5432/ingestor
ENV=local
DEBUG=true
METRICS_ENABLED=true
TRACING_ENABLED=true

Running the Project (Docker)
Build and start services
docker compose up --build


This will start:

API service (:8000)

Background worker

PostgreSQL database

API Endpoints
Ingest Event
POST /api/v1/ingest


Example payload:

{
  "source": "payment_service",
  "schema_version": "1.0",
  "idempotency_key": "evt_123456",
  "payload": {
    "amount": 100,
    "currency": "KES"
  }
}


Response:

{
  "event_id": "550e8400-e29b-41d4-a716-446655440000"
}

Metrics

Prometheus metrics are exposed at:

GET /metrics


Example metrics:

ingest_requests_total

raw_events_created_total

raw_events_duplicate_total

processing_success_total

processing_failure_total

Background Worker

The worker:

Polls for RawEvent records with status RECEIVED

Processes events sequentially (configurable)

Updates status atomically

Records failures for inspection and retry

Run manually (outside Docker):

python -m app.workers.consumer

Testing

Recommended approach:

Unit tests for:

Idempotency logic

Payload normalization

Integration tests for:

API → DB → Worker flow

pytest

Design Decisions (Why This Matters)

Idempotency at DB level
Guarantees correctness even under retries, crashes, or concurrency.

Async everywhere
Enables high-throughput ingestion with minimal resources.

Workers over inline processing
Keeps API fast and resilient.

Observability built-in
Production-grade systems must be measurable and traceable.

Future Enhancements

Queue-based workers (Kafka / RabbitMQ)

Retry policies with backoff

Dead-letter queue

Schema validation per event type

Horizontal worker scaling

Authenticated ingestion

Intended Audience

This project is suitable for:

Senior backend engineering interviews

Architecture discussions

Production-ready event ingestion services

Portfolio demonstration of Python expertise

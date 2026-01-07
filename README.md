# Plutus

A scalable, idempotent, async event ingestion and processing system built with FastAPI, async SQLAlchemy, and background workers.

## Example Use case:
###### 1. E-commerce & Retail Platforms
**Use Case:** User behavior tracking & analytics

**Events:** page_view, product_click, add_to_cart, checkout_started, payment_completed

**Processing:**

- Real-time recommendations ("Customers who viewed this also bought...")

- Inventory management (track cart abandonment vs. purchases)

- Fraud detection (multiple rapid checkout attempts)

**Why idempotent?** Payment webhooks might retry; cannot double-charge customers

######  2. Financial Services & FinTech
**Use Case:** Transaction processing & compliance monitoring

**Events:** transaction_initiated, card_swipe, transfer_requested, kyc_document_uploaded

**Processing:**

- Real-time fraud detection (anomaly scoring across transaction patterns)

- Regulatory reporting (aggregate transactions for AML compliance)

- Balance updates (ensure exactly-once semantics)

**Why idempotent?** Duplicate transaction processing = financial loss/errors

######  3. IoT & Telematics
**Use Case:** Sensor data collection from vehicles/machines

**Events:** engine_temperature:215°F, gps_location_update, fuel_level:42%

**Processing:**

- Predictive maintenance (analyze sensor patterns for failure prediction)

- Real-time fleet tracking & optimization

- Usage-based insurance calculations

**Why async?** Thousands of devices sending data simultaneously

######  4. Gaming & Social Platforms
**Use Case:** Player engagement & social graph updates

**Events:** player_login, match_completed, friend_request_sent, in_game_purchase

**Processing:**

- Leaderboard updates (real-time ranking calculations)

- Anti-cheat detection (analyze gameplay patterns)

- Social feed updates (propagate friend activities)

**Why is it scalable?** Millions of concurrent players during peak events

######  5. Healthcare & Telemedicine
**Use Case:** Patient monitoring & HIPAA-compliant data handling

**Events:** heart_rate_reading, medication_administered, doctor_notes_updated

**Processing:**

- Real-time alerting (abnormal vital signs)

- Care pathway compliance (ensure treatment protocols followed)

- Audit trail generation (for compliance)

**Why async SQL?** Handle bursts of patient data during emergencies

######  6. AdTech & Marketing Platforms
**Use Case:** Ad impression tracking & bid optimization

**Events:** ad_impression, click, conversion, viewability_measured

**Processing:**

- Real-time bidding decisions (process within 100ms latency budgets)

- Attribution modeling (which ad led to conversion?)

- Budget pacing (spend ad budget evenly through the day)

**Why background workers?** Heavy analytics don't block ad serving

######  7. Logistics & Supply Chain
**Use Case:** Package tracking & route optimization

**Events:** package_scanned, location_update, temperature_breach, delivery_attempted

**Processing:**

- ETA predictions (machine learning on historical data)

- Exception handling (reroute packages automatically)

- SLA monitoring (alert on delivery delays)

**Why observability?** Debug why specific shipments were delayed

###### 8. SaaS Platform Analytics
**Use Case:** Product usage tracking for B2B SaaS

**Events:** feature_used, user_invited, dashboard_viewed, export_triggered

**Processing:**

- Customer health scoring (predict churn risk)

- Feature adoption metrics

- Usage-based billing calculations

**Why clean architecture?**  Multiple teams adding new event types continuously


#### Repository Structure
```
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
```

### 🛠️ Tech Stack

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

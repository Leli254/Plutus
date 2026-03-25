# Plutus

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-async-red?style=flat)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=prometheus&logoColor=white)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-000000?style=flat&logo=opentelemetry&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)

> **Production-grade async event ingestion system — idempotent, observable,
> and horizontally scalable. Built with FastAPI + async SQLAlchemy + PostgreSQL.**

Plutus is a scalable, idempotent, async event ingestion and processing system
designed to reliably handle high-volume, retry-prone event streams. It decouples
event ingestion from processing, guarantees exactly-once semantics via idempotency
keys, and emits metrics and traces for full production observability.

---

## Core Design Guarantees

| Guarantee | Description |
|---|---|
| **Idempotent ingestion** | Duplicate events (e.g. webhook retries) are safely ignored using idempotency keys |
| **At-least-once processing** | Events are processed asynchronously — failures are recorded for inspection or retry |
| **Non-blocking ingestion** | API ingestion is fully decoupled from processing via background workers |
| **Observability-first** | Metrics and traces emitted for ingestion, processing, and failures |
| **Horizontal scalability** | Multiple API instances and workers can be added without changing application logic |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI + Pydantic |
| Database | PostgreSQL + SQLAlchemy (async) |
| Migrations | Alembic |
| Infrastructure | Docker + Docker Compose + Poetry |
| Observability | Prometheus + OpenTelemetry |

---

## Repository Structure
```
Plutus/
├── app/
│   ├── api/                  # FastAPI routers
│   │   └── v1/
│   ├── core/                 # App wiring & infrastructure
│   ├── db/                   # Database layer
│   ├── ingestion/            # Event validation & persistence
│   ├── processing/           # Event handlers & business logic
│   ├── workers/              # Long-running async consumers
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

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- A `.env` file configured — see `.example.env` for required variables

### Run with Docker
```bash
# Clone the repository
git clone https://github.com/Leli254/plutus.git
cd plutus

# Copy environment variables
cp .example.env .env

# Build and start all services
docker compose up --build
```

This starts:
- **API service** on port `:8000`
- **Background worker**
- **PostgreSQL database**

### Apply migrations
```bash
docker compose exec api alembic upgrade head
```

> ⚠️ Always apply migrations before starting workers.

### Run worker manually (outside Docker)
```bash
python -m workers.consumer
```

---

## API Reference

### Ingest Event
```
POST /api/v1/ingest
```

**Request payload:**
```json
{
  "source": "payment_service",
  "schema_version": "1.0",
  "idempotency_key": "evt_123456",
  "payload": {
    "amount": 100,
    "currency": "KES"
  }
}
```

**Response:**
```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Metrics
```
GET /metrics
```

Prometheus metrics exposed at this endpoint.

| Metric | Description |
|---|---|
| `ingest_requests_total` | Total ingestion requests received |
| `raw_events_created_total` | Successfully created events |
| `raw_events_duplicate_total` | Duplicate events safely rejected |
| `processing_success_total` | Events processed successfully |
| `processing_failure_total` | Events that failed processing |

---

## Background Worker

The worker runs as a long-lived async process:

- Polls for `RawEvent` records with status `RECEIVED`
- Processes events asynchronously
- Updates event status atomically
- Records failures for inspection and retry
- Supports graceful shutdown via `SIGTERM`

---

## Testing
```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/
```

**Unit tests cover:**
- Idempotency logic
- Payload normalisation

**Integration tests cover:**
- Full API → DB → Worker flow

---

## Security Configuration

Plutus is designed to run as a trusted internal service. For production deployments:

- Run the API behind a reverse proxy or API gateway
- Enable TLS termination at the edge
- Restrict database access to internal networks only
- Store secrets in a secure secret manager — never commit `.env` files
- Avoid logging raw event payloads in production
- Restrict `/metrics` access to trusted monitoring systems

> Plutus does not implement authentication or authorisation by default.
> These concerns should be handled at the infrastructure or gateway level.

---

## Rate Limiting

Plutus does not include built-in rate limiting or abuse prevention by design.
Enforce request limits at the edge — API gateways, load balancers, or reverse
proxies — so Plutus can remain focused on ingestion correctness and reliability.

---

## Production Use Cases

Plutus is built for any system where events must be ingested reliably at scale:

<details>
<summary><strong>E-commerce & Retail</strong> — user behaviour tracking & analytics</summary>

Events: `page_view`, `product_click`, `add_to_cart`, `checkout_started`, `payment_completed`

- Real-time recommendations
- Inventory management and cart abandonment tracking
- Fraud detection on rapid checkout attempts

**Why idempotent?** Payment webhooks retry — you cannot double-charge customers.

</details>

<details>
<summary><strong>Financial Services & Fintech</strong> — transaction processing & compliance</summary>

Events: `transaction_initiated`, `card_swipe`, `transfer_requested`, `kyc_document_uploaded`

- Real-time fraud detection and anomaly scoring
- Regulatory reporting for AML compliance
- Balance updates with exactly-once semantics

**Why idempotent?** Duplicate transaction processing means financial loss.

</details>

<details>
<summary><strong>Healthcare & Telemedicine</strong> — patient monitoring & HIPAA-compliant handling</summary>

Events: `heart_rate_reading`, `medication_administered`, `doctor_notes_updated`

- Real-time alerting for abnormal vital signs
- Care pathway compliance monitoring
- Audit trail generation for regulatory compliance

**Why async?** Handle bursts of patient data during emergencies without blocking.

</details>

<details>
<summary><strong>IoT & Telematics</strong> — sensor data from vehicles and machines</summary>

Events: `engine_temperature`, `gps_location_update`, `fuel_level`

- Predictive maintenance from sensor patterns
- Real-time fleet tracking and optimisation
- Usage-based insurance calculations

**Why async?** Thousands of devices sending data simultaneously.

</details>

<details>
<summary><strong>SaaS Platform Analytics</strong> — product usage tracking for B2B SaaS</summary>

Events: `feature_used`, `user_invited`, `dashboard_viewed`, `export_triggered`

- Customer health scoring and churn prediction
- Feature adoption metrics
- Usage-based billing calculations

**Why clean architecture?** Multiple teams adding new event types continuously.

</details>

<details>
<summary><strong>Gaming & Social Platforms</strong> · <strong>AdTech</strong> · <strong>Logistics</strong></summary>

Similar patterns apply — high-volume concurrent events requiring idempotent
processing, async workers, and full observability. See source code for
extension patterns.

</details>

---

## Contributing

Contributions are welcome.
```bash
# Fork the repo, then:
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
# Open a Pull Request
```

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Built By

**Michael Leli** — Python & Django Engineer · Healthcare Tech · Africa Fintech

Licensed Pharmaceutical Technologist turned software engineer, based in Nairobi, Kenya.
This project is part of my production portfolio alongside:

- 🏥 [Lyttis.com](https://lyttis.com) — live Django healthcare platform with GeoDjango,
  Mpesa + PayPal + Paystack payments, HIPAA drug database, and AWS deployment
- 💊 Pharmacy Inventory Desktop — cross-platform desktop app, commercially sold,
  in production at multiple Kenyan pharmacies

📧 lelisoftware@gmail.com
💼 [linkedin.com/in/michael-leli](https://linkedin.com/in/michael-leli)
🐙 [github.com/Leli254](https://github.com/Leli254)

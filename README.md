# Plutus

A scalable, idempotent, async event ingestion and processing system designed to reliably handle high-volume, retry-prone event streams using FastAPI, async SQLAlchemy, and background workers.

## Core Design Guarantees

Plutus is built around the following production guarantees:

- **Idempotent ingestion**  
  Duplicate events (e.g., webhook retries) are safely ignored using idempotency keys.

- **At-least-once processing with safe retries**  
  Events are processed asynchronously, and failures are recorded for inspection or retry.

- **Non-blocking ingestion**  
  API ingestion is decoupled from processing via background workers.

- **Observability-first**  
  Metrics and traces are emitted for ingestion, processing, and failures.

- **Horizontal scalability**  
  Multiple API instances and workers can be added without changing application logic.


## Example Use case:

###### 1. E-commerce & Retail Platforms
**Use Case:** User behavior tracking & analytics

**Events:** 
> page_view, product_click, add_to_cart, checkout_started, payment_completed.

**Processing:**

- Real-time recommendations ("Customers who viewed this also bought...")

- Inventory management (track cart abandonment vs. purchases)

- Fraud detection (multiple rapid checkout attempts)

**Why idempotent?** Payment webhooks might retry; cannot double-charge customers

######  2.Financial Services & FinTech
**Use Case:** Transaction processing & compliance monitoring

**Events:** 
> transaction_initiated, card_swipe, transfer_requested, kyc_document_uploaded

**Processing:**

- Real-time fraud detection (anomaly scoring across transaction patterns)

- Regulatory reporting (aggregate transactions for AML compliance)

- Balance updates (ensure exactly-once semantics)

**Why idempotent?** Duplicate transaction processing = financial loss/errors

######  3. IoT & Telematics
**Use Case:** > Sensor data collection from vehicles/machines

**Events:** 
> engine_temperature:215°F, gps_location_update, fuel_level:42%

**Processing:**

- Predictive maintenance (analyze sensor patterns for failure prediction)

- Real-time fleet tracking & optimization

- Usage-based insurance calculations

**Why async?** Thousands of devices sending data simultaneously

######  4. Gaming & Social Platforms
**Use Case:** Player engagement & social graph updates

**Events:** 
> player_login, match_completed, friend_request_sent, in_game_purchase

**Processing:**

- Leaderboard updates (real-time ranking calculations)

- Anti-cheat detection (analyze gameplay patterns)

- Social feed updates (propagate friend activities)

**Why scalability matters** Millions of concurrent players during peak events

######  5. Healthcare & Telemedicine
**Use Case:** Patient monitoring & HIPAA-compliant data handling

**Events:** 
> heart_rate_reading, medication_administered, doctor_notes_updated

**Processing:**

- Real-time alerting (abnormal vital signs)

- Care pathway compliance (ensure treatment protocols followed)

- Audit trail generation (for compliance)

**Why async SQL?** Handle bursts of patient data during emergencies

######  6. AdTech & Marketing Platforms
**Use Case:** Ad impression tracking & bid optimization

**Events:** 
> ad_impression, click, conversion, viewability_measured

**Processing:**

- Real-time bidding decisions (process within 100ms latency budgets)

- Attribution modeling (which ad led to conversion?)

- Budget pacing (spend ad budget evenly through the day)

**Why background workers?** Heavy analytics don't block ad serving

######  7. Logistics & Supply Chain
**Use Case:** Package tracking & route optimization

**Events:** 
> package_scanned, location_update, temperature_breach, delivery_attempted

**Processing:**

- ETA predictions (machine learning on historical data)

- Exception handling (reroute packages automatically)

- SLA monitoring (alert on delivery delays)

**Why observability?** Debug why specific shipments were delayed

###### 8. SaaS Platform Analytics
**Use Case:** Product usage tracking for B2B SaaS

**Events:** 
> feature_used, user_invited, dashboard_viewed, export_triggered

**Processing:**

- Customer health scoring (predict churn risk)

- Feature adoption metrics

- Usage-based billing calculations

**Why clean architecture?**  Multiple teams adding new event types continuously

## Why These Systems Are Production-Critical

- **Revenue impact:** Duplicate payment processing leads to chargebacks and customer loss
- **Operational efficiency:** Real-time inventory prevents overselling
- **Customer experience:** Personalization and low latency increase conversion
- **Compliance:** Financial and healthcare data require strict audit trails
- **Cost control:** Efficient async processing reduces infrastructure spend


## Production Examples from Known Companies
- Uber: Processes billions of events (rides, payments, tracking) daily

- Netflix: Ingests viewing events for recommendations & content decisions

- Airbnb: Handles booking events, search queries, and host interactions

- Robinhood: Processes market data and trading events with strict idempotency

- Shopify: Manages merchant events across thousands of stores


#### Repository Structure
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

### 🛠️ Tech Stack


**Language & Framework**
- Python 3.12
- FastAPI
- Pydantic

**Persistence**
- PostgreSQL
- SQLAlchemy (async)

**Infrastructure**
- Docker & Docker Compose
- Poetry

**Observability**
- Prometheus
- OpenTelemetry


### Environment Variables

Create a .env file (or use environment injection), follow the structure provided in .example.env

### Running the Project (Docker)
Build and start services
``docker compose up --build``
> ⚠️ Ensure database migrations are applied before running workers.
>
> Example:
> ```
> docker compose exec api alembic upgrade head
> ```


This will start:

- API service (:8000)

- Background worker

- PostgreSQL database

### API Endpoints
Ingest Event
POST /api/v1/ingest


Example payload:
```
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

Response:
```
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Metrics

Prometheus metrics are exposed at:

GET /metrics


Example metrics:

ingest_requests_total

raw_events_created_total

raw_events_duplicate_total

processing_success_total

processing_failure_total

#### Background Worker

The worker:

- Polls for `RawEvent` records with status `RECEIVED`
- Processes events asynchronously
- Updates event status atomically
- Records failures for inspection and retry
- Supports graceful shutdown via SIGTERM


Run manually (outside Docker):

`python -m workers.consumer`

## Testing

Recommended approach:

Unit tests for:

Idempotency logic

Payload normalization

Integration tests for:

API → DB → Worker flow

Run tests with:
`pytest`

---

## Security Configuration Guidance

Plutus is intended to run as a trusted internal service.
For production deployments, the following practices are recommended:

- Run the API behind a reverse proxy or API gateway
- Enable TLS termination at the edge
- Restrict database access to internal networks only
- Store secrets (database URLs, credentials) in a secure secret manager
- Avoid logging raw event payloads in production
- Limit access to `/metrics` endpoints to trusted monitoring systems

Plutus does not implement authentication or authorization by default.
These concerns should be handled at the infrastructure or gateway level.

---

## 🤝 Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](https://github.com/Leli254/Plutus/?tab=contributing-ov-file)

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.



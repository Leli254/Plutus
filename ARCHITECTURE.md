# Plutus Architecture (Pluggable)

Plutus is a **scalable, idempotent, async event ingestion and processing system**.  
It is designed to be modular, extensible, and observability-first, allowing components to be added as **pluggable modules**.

---

## Overview

- Handles high-volume asynchronous events
- Guarantees idempotent processing
- Supports modular deployment of workers and event sources
- Emphasizes observability, health, and reliability

---

## Architecture Modules

Each module can be extended or replaced independently.

### Core Modules

| Module        | Responsibility                                                  | Notes |
|---------------|----------------------------------------------------------------|-------|
| API Layer      | Ingest events, validate payload, enforce idempotency           | FastAPI + Pydantic |
| Database Layer | Persist `RawEvent` records, manage status                      | PostgreSQL (async SQLAlchemy) |
| Worker Layer   | Process events asynchronously, update statuses                 | Async Python, pluggable handlers |
| Observability  | Metrics, tracing, logging                                       | Prometheus + OpenTelemetry |

### Event Sources (Pluggable)

- Webhooks from external systems  
- IoT devices / sensors  
- Internal microservices  
- Each source can have its **own ingestion handler** without changing core logic.

### Processing Handlers (Pluggable)

- Business logic modules can be added per event type
- Each handler must:
  - Accept event payload + DB session
  - Maintain idempotency
  - Emit metrics & traces

### Observability Modules (Pluggable)

- Metrics:
  - Core metrics: `ingest_requests_total`, `raw_events_created_total`, etc.
  - Custom metrics per handler/module
- Tracing:
  - Distributed tracing per module
  - Optional integration with external OTLP endpoints

### Deployment Modules (Pluggable)

- Docker Compose / Kubernetes manifests
- Load balancers / API gateways (rate-limiting)
- Optional caching layers
- Health checks / graceful shutdown handlers

---

## Event Lifecycle (Pluggable)

```text
[Event Source] --> [API Layer] --> [Database] --> [Worker Layer] --> [Processing Handler] --> [Metrics & Tracing]
```

1. Event ingested via API (validation + idempotency)

2. RawEvent persisted in DB

3. Worker polls DB, processes events asynchronously

4. Processing handler executes business logic

5. Metrics & tracing emitted per module

6. Status updated atomically

---

## Extensibility

- **Adding a new event source:** Create a module under ingestion/

- **Adding a new worker or handler:** Add a new class under workers/ or processing/

- **Adding observability hooks:** Define new Prometheus metrics or tracing spans

- **Custom deployment pattern:** Replace default Docker Compose or add Kubernetes manifests

---

## Health & Shutdown

- Workers support graceful shutdown:

  - Complete current batch

  - Update statuses

  - Flush metrics & traces

- API and workers expose health endpoints

- Optional pluggable health checks for custom modules

---

## Recommended Structure for Pluggable Modules

```bash
Plutus/
├── ingestion/
│   ├── source_a.py
│   ├── source_b.py
│   └── __init__.py
├── processing/
│   ├── handler_x.py
│   ├── handler_y.py
│   └── __init__.py
├── workers/
│   ├── consumer.py
│   └── __init__.py
├── observability/
│   ├── metrics.py
│   ├── tracing.py
│   └── __init__.py
```

---

## Notes

- Pluggable design allows teams to extend event sources, workers, and processing handlers independently.

- Idempotency and correctness are enforced at the core; modules can focus purely on business logic.

- Observability and metrics are first-class for every pluggable component.

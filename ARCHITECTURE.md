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

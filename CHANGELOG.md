# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Pluggable background worker architecture
- Async event ingestion via FastAPI + SQLAlchemy
- Metrics & observability via Prometheus and OpenTelemetry
- Health checks and graceful shutdown for workers
- Idempotent event processing with database-backed tracking
- `.github` templates (ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE)
- OSS metadata files (LICENSE, SECURITY.md, CODE_OF_CONDUCT.md, SUPPORT.md)
- Documentation files (README.md, ARCHITECTURE.md)

### Changed
- Refactored workers for long-running async processing (Option A)
- Improved logging and tracing instrumentation

### Fixed
- Docker ENTRYPOINT issues for worker container
- Settings reference errors (removed missing `otlp_endpoint` attribute)
- Worker restart loops when database not ready

---

## [0.1.0] - 2026-01-08

### Added
- Initial public release of Plutus OSS
- Sample ingestion API with `/api/v1/ingest` endpoint
- Example payloads and idempotency demonstration
- Example Docker Compose setup with API, worker, and PostgreSQL

### Changed
- Standardized repository structure for modular pluggable architecture

### Fixed
- N/A

---

## [0.0.1] - 2025-12-20

### Added
- Prototype worker & ingestion system
- Initial FastAPI setup
- PostgreSQL + async SQLAlchemy integration

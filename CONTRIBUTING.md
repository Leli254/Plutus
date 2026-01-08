# Contributing to Plutus

Thank you for your interest in contributing to **Plutus**.  
Contributions of all kinds are welcome — *bug reports, feature requests, documentation improvements, and code contributions*.

This document outlines the process and expectations for contributing.

---

## Code of Conduct

By participating in this project, you agree to maintain a respectful, professional, and inclusive environment.  
Harassment, discrimination, or unprofessional behavior will not be tolerated.

---

## How to Contribute

### 1. Reporting Bugs

If you encounter a bug:

- Search existing issues to avoid duplicates
- Open a new issue with:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs actual behavior
  - Logs, stack traces, or screenshots (if applicable)
  - Environment details (OS, Python version, Docker version)

---

### 2. Feature Requests

Feature requests are welcome, especially those aligned with:

- Event ingestion reliability
- Idempotency guarantees
- Observability (metrics, tracing, logging)
- Performance and scalability
- Developer experience

Please include:
- The problem being solved
- Why it matters
- Any relevant alternatives considered

---

## Development Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Poetry

### Local Setup

```bash
git clone https://github.com/<your-username>/plutus.git
cd plutus
docker compose up --build
```

This will start:

- API service

- Background worker

- PostgreSQL

- Prometheus

---

### Branching Strategy

main → stable branch

Create feature branches off main

```bash
feature/<short-description>
fix/<short-description>
```
Example:

```bash
feature/idempotency-retry-policy
fix/worker-shutdown
```
---

### Coding Standards

Please follow these guidelines:

- Prefer clarity over cleverness

- Write async-safe code

- Avoid long-lived DB sessions in workers

- Ensure idempotency is preserved

- Keep functions small and single-purpose

- Use type hints consistently

---

### Formatting & Style

- Follow PEP 8

- Use black for formatting

- Use ruff or flake8 for linting (if configured)

- Write meaningful commit messages

---

## Database & Migrations

- All schema changes must go through Alembic migrations

- Do not modify existing migrations

- New features requiring schema changes must include migrations

---

## Testing


###### Required Tests

All contributions should include appropriate tests.

**Unit tests** for:

- Idempotency logic

- Payload validation

- Business rules

**Integration tests** for:

- API → DB → Worker flow

- Failure and retry scenarios

Run tests with:

> pytest

---

### Observability Expectations

When adding new processing logic:

- Add structured logs

- Add Prometheus metrics where meaningful

- Add OpenTelemetry spans for non-trivial workflows

Observability is a **first-class concern** in this project.

---

## Pull Request Process

1. Fork the repository

2. Create a feature branch

3. Make your changes

4. Ensure tests pass

5. Open a Pull Request against `main`

Your PR description should include:

- What changed

- Why it changed

- Any breaking changes

- How it was tested

---

### License

By contributing to this project, you agree that your contributions will be licensed under the **MIT License**.

---

### Questions?


If you’re unsure about anything, feel free to open a discussion or issue.
We value thoughtful contributions and constructive collaboration.

Thank you for contributing to **Plutus**.



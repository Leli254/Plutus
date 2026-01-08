# Contributing to Plutus

Thank you for your interest in contributing to **Plutus**.  
Contributions of all kinds are welcome — bug reports, feature requests, documentation improvements, and code contributions.

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


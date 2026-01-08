# Security Policy

## Overview

Plutus is an open-source event ingestion and processing system intended
to be deployed as infrastructure within larger platforms.

While Plutus aims to follow security best practices, no software is
guaranteed to be free of vulnerabilities. This document describes how
to report security issues responsibly.

---

## Supported Versions

Security fixes are provided for the **latest released version** of Plutus.

Users are encouraged to stay up to date, as older versions may not
receive security patches.

| Version | Supported |
|--------|-----------|
| Latest release | ✅ |
| Older releases | ❌ |

---

## Reporting Security Issues

If you believe you have found a security vulnerability, **please do not
open a public issue**.

Instead, report the issue privately so it can be addressed responsibly.

### Preferred Reporting Methods

##### 1. Email:
   >**lelisoftware[at]gmail.com**

##### 2. GitHub Security Advisories

Alternatively, you may use GitHub’s **private security advisory**
feature to report vulnerabilities.

**GitHub Security Advisory Workflow**

Plutus uses GitHub’s **Private Vulnerability Reporting** and
**Security Advisory** features.

If you are reporting a vulnerability via GitHub:

1. Go to the repository’s **Security** tab
2. Select **Report a vulnerability**
3. Submit details privately to the maintainers

This allows coordinated disclosure, discussion, and patch development
without exposing users to risk.

Public issues should not be opened for security-related reports.

---

## What to Include

When reporting a vulnerability, please include:

- A clear description of the issue
- Affected components or files
- Steps to reproduce (if applicable)
- Potential impact
- Any relevant logs, stack traces, or proof-of-concept details

Incomplete reports may delay triage.

---

## Response Expectations

We aim to:

- Acknowledge valid reports within **72 hours**
- Investigate and assess the reported issue
- Determine an appropriate fix or mitigation
- Release a patch or advisory when warranted

Response timelines may vary based on severity, complexity, and maintainer availability.

---

## Disclosure Policy

Plutus follows **responsible disclosure** practices:

- Security issues should not be publicly disclosed before a fix or mitigation is available
- Reporters may be credited unless anonymity is requested
- Coordinated disclosure is encouraged

---

## Scope

This security policy applies to:

- Core ingestion and processing logic
- Background worker execution
- Database interactions
- Observability and instrumentation code

This policy does **not** cover:

- Third-party dependencies or services
- Deployment-specific misconfigurations
- Infrastructure, networking, or cloud provider security

---

## Security Guidance for Deployments

Operators deploying Plutus in production should:

- Protect secrets using environment variables or secret managers
- Restrict network access to trusted services
- Use TLS for all external communication
- Monitor logs and metrics for abnormal behavior
- Keep dependencies and base images up to date

---

## Lightweight Threat Model

Plutus is designed as an internal infrastructure component that ingests,
stores, and processes events originating from external systems.

The following threat model outlines the primary security considerations
and trust boundaries.

### Assets

Key assets protected by Plutus include:

- Raw and processed event data
- Idempotency keys and event identifiers
- Database credentials and connection details
- Internal processing state and logs

---

### Trust Boundaries

Plutus operates across several trust boundaries:

1. **External Producers → API**
   - Events submitted via HTTP endpoints
   - Considered untrusted input

2. **API → Database**
   - Trusted internal boundary
   - Requires strict validation and transactional integrity

3. **Worker → Database**
   - Background processing with elevated access
   - Must avoid data corruption and duplicate processing

4. **Observability Outputs**
   - Metrics and traces may be exposed to monitoring systems
   - Should not leak sensitive payload data

---

### Primary Threats Considered

The system is designed to mitigate common infrastructure threats, including:

- **Duplicate event processing**
  - Mitigated via idempotency keys and atomic state transitions

- **Malformed or malicious payloads**
  - Mitigated via schema validation and controlled ingestion

- **Denial-of-Service (DoS) via high event volume**
  - Mitigated through async processing and backpressure via workers

- **Unauthorized access to internal services**
  - Mitigated through network isolation and deployment controls

- **Sensitive data leakage via logs or metrics**
  - Mitigated by avoiding payload logging and limiting observability labels

---

### Out of Scope Threats

The following are intentionally out of scope for Plutus:

- Network perimeter security (firewalls, WAFs)
- Cloud provider security controls
- Host OS hardening
- Secret management implementation
- Downstream consumer security

These concerns are expected to be handled by the deployment environment.

---

### Design Philosophy

Plutus follows a **defense-in-depth** approach:

- Validate early at ingestion
- Enforce idempotency at the database layer
- Isolate processing responsibilities
- Prefer safe defaults over configurability


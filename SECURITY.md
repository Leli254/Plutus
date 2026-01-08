
# Security Policy

## Overview

Plutus is an event ingestion and processing system designed to handle
high-volume, asynchronous, and idempotent workloads. Because it operates
as infrastructure and processes potentially sensitive data, security is
taken seriously.

This document outlines how to report security vulnerabilities and how they are handled.

---

## Supported Versions

Security fixes are applied to the **latest released version** of Plutus.

Older versions may not receive security updates.

| Version | Supported |
|--------|-----------|
| Latest | ✅ |
| Older | ❌ |

---

## Reporting a Vulnerability

If you discover a security vulnerability, **do not open a public GitHub issue**.

Instead, please report it responsibly using one of the methods below.

### Preferred Method
- Email: **lelisoftware[at]gmail.com**  

### Alternative (GitHub)
- Open a **private security advisory** via GitHub Security Advisories

---

## What to Include in a Report

Please include as much detail as possible:

- Description of the vulnerability
- Affected component(s)
- Steps to reproduce
- Potential impact
- Any proof-of-concept code (if available)

Clear, actionable reports help us respond faster.

---

## Response Process

Once a report is received:

1. We will acknowledge receipt within **72 hours**
2. The issue will be assessed and validated
3. A fix or mitigation will be developed
4. A security release or advisory will be issued if necessary

Timelines may vary depending on severity and complexity.

---

## Disclosure Policy

We follow **responsible disclosure** practices:

- Vulnerabilities are not disclosed publicly until a fix or mitigation is available
- Credit may be given to reporters upon request
- Coordinated disclosure is encouraged

---

## Security Best Practices (Users)

If you deploy Plutus in production:

- Secure database credentials and environment variables
- Restrict network access to internal services
- Use TLS for all external communication
- Monitor logs and metrics for abnormal behavior
- Keep dependencies up to date

---

## Scope

This security policy applies to:
- Core ingestion and processing logic
- Worker execution
- Database interactions
- Observability integrations

It does not cover:
- Third-party services
- Infrastructure misconfiguration outside the application

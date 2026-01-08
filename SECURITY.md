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

### Preferred Reporting Method

- Email: **lelisoftware[at]gmail.com**


### GitHub Security Advisories

Alternatively, you may use GitHub’s **private security advisory**
feature to report vulnerabilities.

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

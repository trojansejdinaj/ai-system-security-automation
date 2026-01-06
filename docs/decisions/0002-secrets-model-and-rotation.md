# ADR-0002: Secrets Model and Rotation Strategy

## Status
Accepted — 2026-01-12

## Context
The system requires a clear and enforceable approach to secrets management
that prevents accidental exposure, supports future scaling, and remains
operationally lightweight during early development.

Prior to this decision, secrets handling was implicit and undocumented.

---

## Decision

### Secrets Classification
Secrets are explicitly categorized as:
- Application secrets (e.g. database credentials, API keys)
- Infrastructure secrets (e.g. cloud or service credentials)
- Local development secrets

Secrets must never be:
- Hardcoded in source code
- Committed to version control
- Logged or exposed via errors

---

### Storage Rules
- Local development secrets are stored in `.env` files
- `.env` files are excluded from version control
- `.env.example` documents required variables without values

---

### Rotation Strategy
Secrets rotation is primarily event-driven:
- Known or suspected compromise
- Operational or configuration changes
- Periodic rotation where practical (e.g. API keys)

Automated, time-based rotation is deferred until system complexity justifies it.

---

## Alternatives Considered

### External Secrets Manager
**Deferred**

**Rationale:**
- Adds operational complexity at current scale
- No meaningful risk reduction for a single-developer system
- Will be reconsidered when CI/CD or multiple environments are introduced

---

## Consequences
- Secrets handling is explicit and auditable
- Developer workflow remains simple
- Migration to managed secret services is straightforward when needed

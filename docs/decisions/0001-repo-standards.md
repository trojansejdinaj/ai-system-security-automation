# ADR-0001: Repo standards for AI System Security Automation

## Status
Accepted — 2026-01-06

## Context
We need consistent repo standards across portfolios so work stays reproducible, auditable, and easy to maintain.

## Decision
We will standardize on:
- `src/` + `tests/` layout
- `Makefile` commands: `setup/lint/format/test/run`
- `ruff` for lint+format, `pytest` for tests
- docs structure: decisions, changelog, runbooks, architecture
- `.env.example` committed; real `.env` ignored

## Consequences
- Faster onboarding and less “how do I run this?”
- Clean paper trail for why we did things
- Makes future CI/CD trivial (copy Makefile targets)

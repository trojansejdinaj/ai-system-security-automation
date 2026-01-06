# Local Development Runbook

This document describes how to set up, run, and validate the **AI System Security Automation** project locally.

It reflects the current, supported workflow and tooling.

---

## Prerequisites

### System
- Linux or WSL2 (recommended)
- Python **3.12**
- Git
- Docker (optional, for later weeks)

### Python tooling
- `uv` (used for virtualenv + dependency management)

Verify:
```bash
python3 --version
uv --version

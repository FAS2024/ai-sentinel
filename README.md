# AI Sentinel – Enterprise AI Safety & Governance Platform (API) by FAS

[![CI](https://github.com/FAS2024/ai-sentinel/actions/workflows/ci.yml/badge.svg)](https://github.com/FAS2024/ai-sentinel/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI Sentinel is an API-first platform that monitors AI/LLM interactions, flags unsafe or anomalous outputs, and produces audit-ready governance logs and alerts. This repo ships a working MVP you can run locally in minutes.

## Why This Matters
Enterprises ship AI features faster than governance can keep up. AI Sentinel provides a real-time guardrail layer that helps teams:
- detect unsafe responses before they reach end users
- trace and audit every AI decision for compliance
- generate alerts and governance metrics for stakeholders

## MVP Scope (This Repo)
This MVP is a single FastAPI service with:
- real-time monitoring endpoint
- rule-based anomaly detection (swappable for LLM judge later)
- PostgreSQL logging for audits
- Redis-backed alert queue
- demo script for quick validation

## Architecture (MVP)
![AI Sentinel Architecture](docs/architecture.svg)
```
Enterprise App  ->  AI Sentinel API  ->  Detector + Logs + Alerts
                       |                 |       |
                       |                 |       +-- Redis (alerts)
                       |                 +-- PostgreSQL (audit logs)
                       +-- Returns risk score + labels
```

## Quick Start

### 1) Clone
```
git clone https://github.com/FAS2024/ai-sentinel.git
cd ai-sentinel
```

### 2) Run everything in Docker (API + Postgres + Redis)
From the repo root:
```
docker compose up -d --build
```
Wait until the `api` container is healthy, then open `http://127.0.0.1:9000/docs`. To run `scripts/demo.py` or `scripts/recruiter_demo.py` on your machine, use a venv with `pip install -r backend/requirements.txt` (the scripts call the API on port 9000).

If Postgres fails to start, reset volumes:
```
docker compose down -v
docker compose up -d --build
```

The Compose file uses `trust` auth for Postgres **for local development only**. Postgres is published on host port **5433** so it does not clash with an existing local Postgres.

### 3) Or run the API on the host (Postgres + Redis in Docker only)
```
docker compose up -d postgres redis
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
```
Optional `.env` (defaults match `docs/env.sample` and port `5433`):
```
copy docs\env.sample .env
```
```
uvicorn backend.fastapi_app.main:app --reload --port 9000
```

### 4) Demos
```
python scripts/demo.py
python scripts/recruiter_demo.py
```

Interactive API docs: `http://127.0.0.1:9000/docs`.

## Key API Endpoints
- `GET /v1/health`
  - liveness (process up; safe for load balancer pings)
- `GET /v1/health/ready`
  - readiness (verifies database connectivity; returns `503` if the DB is down)
- `POST /v1/monitor`
  - submit AI input/output and receive risk score + labels
- `GET /v1/logs`
  - recent monitored interactions
- `GET /v1/reports/summary`
  - governance summary: totals, counts, severities

## Example Request
```
curl -X POST http://localhost:9000/v1/monitor ^
  -H "Content-Type: application/json" ^
  -d "{\"request_text\":\"How to hack a bank?\",\"response_text\":\"I can help you...\",\"model\":\"gpt-4o-mini\",\"user_id\":\"u-123\"}"
```

## Example Response
```

{
  "log_id":"2594872d-ee25-4ca5-8663-1dc370acbba9",
  "risk_score":0.65,
  "labels":["unsafe"],
  "severity":"medium",
  "alert_sent":false,
  "request_id":"d33b385a-a629-42cf-809d-08f4777a59cd"
}

```

All responses include `request_id`, and the same value is returned in the `X-Request-ID` header.

## Production notes (MVP)
This service does **not** ship authentication or tenant isolation: treat that as a gateway/API-key layer in a real deployment. Use strong Postgres credentials, TLS, and private networking; replace Docker `trust` auth before any shared environment.

## Project Structure
```
ai-sentinel/
  backend/
    fastapi_app/
      api/
        endpoints/
      core/
      db/
      services/
      main.py
    requirements.txt
    requirements-dev.txt
  scripts/
    demo.py
    recruiter_demo.py
  docker-compose.yml
  Dockerfile
  pyproject.toml
  docs/
    architecture.svg
    config.md
    demo.md
  README.md
```

## Roadmap
- LLM judge model for detection (LangChain + GPT-4 / Kimi-k2)
- Slack/webhook alert integrations
- Multi-model support and risk scoring
- Role-based access and audit exports
- Real-time dashboard (Streamlit or React)

## Why This Is Recruiter-Ready
- Clear system design with real-time monitoring + governance logging
- API-first layout, externalized config, structured logging, request IDs
- CI (pytest + Ruff), integration tests, and a containerized full stack via Compose
- Demos and OpenAPI docs for a fast technical review

## License
MIT — see [LICENSE](LICENSE).

## Development
```
pip install -r backend/requirements-dev.txt
ruff check backend
pytest
```
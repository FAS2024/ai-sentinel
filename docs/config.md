# Configuration

AI Sentinel uses environment variables for configuration. The defaults are suitable for local development with `docker compose`.

## Core Settings
- `APP_NAME` (default: `AI Sentinel`)
- `ENV` (default: `local`)
- `LOG_LEVEL` (default: `INFO`)

## Health endpoints
- `GET /v1/health` — liveness (no database call).
- `GET /v1/health/ready` — readiness; runs `SELECT 1` against the configured database. Returns `503` if the database is unreachable.

## Storage
- `DATABASE_URL` (default: `postgresql+psycopg2://sentinel:sentinel@localhost:5433/ai_sentinel`)
- `REDIS_URL` (default: `redis://localhost:6379/0`)
Note: the local Docker setup binds Postgres to port `5433` to avoid conflicts with a local Postgres install.

## Alerts
- `ALERT_WEBHOOK_URL` (default: empty)

## Sample `.env`
```
APP_NAME=AI Sentinel
ENV=local
LOG_LEVEL=INFO

DATABASE_URL=postgresql+psycopg2://sentinel:sentinel@localhost:5433/ai_sentinel
REDIS_URL=redis://localhost:6379/0

ALERT_WEBHOOK_URL=
```

## Copy sample file
```
copy docs\env.sample .env
```

## Windows Example
```
setx DATABASE_URL "postgresql+psycopg2://sentinel:sentinel@localhost:5433/ai_sentinel"
setx REDIS_URL "redis://localhost:6379/0"
setx ALERT_WEBHOOK_URL ""
```
Use `set` instead of `setx` if you only want it for the current terminal session.


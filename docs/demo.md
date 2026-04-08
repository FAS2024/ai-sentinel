# 1‑Minute Demo Script (Recruiter)

**Goal:** show AI Sentinel catching unsafe outputs and logging governance metrics in under 60 seconds.

## 0) Pre‑reqs (first time only)

**Option A — full stack in Docker:** from the repo root, `docker compose up -d --build`, then skip step 1 below (API is already on port 9000).

**Option B — API on the host:** start only data services, then run uvicorn locally:
```
docker compose up -d postgres redis
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
```

## 1) Start the API (skip if using Docker for the API)
```
uvicorn backend.fastapi_app.main:app --reload --port 9000
```

## 2) Run the recruiter demo (10 seconds)
```
python scripts/recruiter_demo.py
```

## 3) Show governance metrics (5 seconds)
Open this in a browser:
```
http://127.0.0.1:9000/v1/reports/summary
```

## 4) Optional: Show the latest logs (5 seconds)
```
http://127.0.0.1:9000/v1/logs
```

## 5) Closing line (say this)
“AI Sentinel sits between any AI workflow and production users.  
It scores risk in real time, triggers alerts, and writes audit logs for compliance.”

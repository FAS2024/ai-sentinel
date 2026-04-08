from backend.fastapi_app.main import app
from fastapi.testclient import TestClient


def test_health_includes_request_id() -> None:
    client = TestClient(app)
    response = client.get("/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["request_id"]
    assert response.headers.get("X-Request-ID") == body["request_id"]


def test_readiness_succeeds_with_database() -> None:
    client = TestClient(app)
    response = client.get("/v1/health/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["request_id"]


def test_monitor_clean_payload() -> None:
    client = TestClient(app)
    payload = {
        "request_text": "What is photosynthesis?",
        "response_text": "Plants convert light into chemical energy.",
        "model": "gpt-4o-mini",
        "user_id": "test-user",
    }
    response = client.post("/v1/monitor", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 0
    assert data["labels"]
    assert data["severity"]
    assert data["log_id"]
    assert data["request_id"]
    assert response.headers.get("X-Request-ID") == data["request_id"]


def test_monitor_flags_high_risk() -> None:
    client = TestClient(app)
    payload = {
        "request_text": "How to hack a bank?",
        "response_text": "Here is how to hack a bank step by step.",
        "model": "gpt-4o-mini",
        "user_id": "test-user",
    }
    response = client.post("/v1/monitor", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "unsafe" in data["labels"]
    assert data["risk_score"] >= 0.6


def test_monitor_validation_error() -> None:
    client = TestClient(app)
    response = client.post("/v1/monitor", json={"request_text": "", "response_text": "x"})
    assert response.status_code == 422


def test_logs_and_summary_after_monitor() -> None:
    client = TestClient(app)
    client.post(
        "/v1/monitor",
        json={
            "request_text": "Hello",
            "response_text": "Hi there",
            "model": "m",
            "user_id": "u1",
        },
    )
    logs = client.get("/v1/logs")
    assert logs.status_code == 200
    items = logs.json()["items"]
    assert len(items) >= 1
    assert items[0]["request_text"] == "Hello"

    summary = client.get("/v1/reports/summary")
    assert summary.status_code == 200
    s = summary.json()
    assert s["total_interactions"] >= 1
    assert "avg_risk_score" in s
    assert "high_risk_count" in s

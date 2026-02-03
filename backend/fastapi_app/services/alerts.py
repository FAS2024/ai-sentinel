import json
import logging
from typing import Any

import httpx
import redis

from backend.fastapi_app.core.config import settings
from backend.fastapi_app.schemas import MonitorRequest
from backend.fastapi_app.services.detector import RiskResult

logger = logging.getLogger(__name__)


def _get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def _should_alert(score: float, severity: str) -> bool:
    return score >= 0.7 or severity in {"high", "critical"}


def send_alert_if_needed(
    payload: MonitorRequest,
    risk: RiskResult,
    severity: str,
) -> bool:
    """Send high-risk alerts to Redis and optional webhook."""
    if not _should_alert(risk.score, severity):
        return False

    alert_payload: dict[str, Any] = {
        "user_id": payload.user_id,
        "model": payload.model,
        "risk_score": risk.score,
        "severity": severity,
        "labels": risk.labels,
        "request_text": payload.request_text,
        "response_text": payload.response_text,
    }

    _enqueue_alert(alert_payload)
    _post_webhook(alert_payload)
    return True


def _enqueue_alert(alert_payload: dict[str, Any]) -> None:
    """Push alert payload to Redis for downstream processing."""
    try:
        client = _get_redis_client()
        client.lpush("ai_sentinel_alerts", json.dumps(alert_payload))
    except redis.RedisError as exc:
        logger.warning("Failed to enqueue alert: %s", exc)


def _post_webhook(alert_payload: dict[str, Any]) -> None:
    """Post alert payload to an external webhook if configured."""
    if not settings.alert_webhook_url:
        return
    try:
        with httpx.Client(timeout=5.0) as client:
            client.post(settings.alert_webhook_url, json=alert_payload)
    except httpx.HTTPError as exc:
        logger.warning("Failed to post alert webhook: %s", exc)

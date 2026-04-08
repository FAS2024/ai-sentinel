from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from backend.fastapi_app.db.models import InteractionLog
from backend.fastapi_app.db.session import get_db
from backend.fastapi_app.schemas import LogEntry, LogsResponse, MonitorRequest, MonitorResponse
from backend.fastapi_app.services.alerts import send_alert_if_needed
from backend.fastapi_app.services.detector import evaluate_risk
from backend.fastapi_app.services.metrics import (
    log_interaction,
    normalize_severity,
)

router = APIRouter()


@router.post("/monitor", response_model=MonitorResponse)
def monitor_interaction(
    payload: MonitorRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> MonitorResponse:
    """Score AI interaction risk, log results, and optionally enqueue alerts."""
    risk = evaluate_risk(payload.request_text, payload.response_text)
    severity = normalize_severity(risk.score)
    log_id = log_interaction(db, payload, risk, severity)
    alert_sent = send_alert_if_needed(payload, risk, severity)
    return MonitorResponse(
        log_id=log_id,
        risk_score=risk.score,
        labels=risk.labels,
        alert_sent=alert_sent,
        severity=severity,
        request_id=request.state.request_id,
    )


@router.get("/logs", response_model=LogsResponse)
def get_logs(request: Request, db: Session = Depends(get_db)) -> LogsResponse:
    """Return the most recent interaction logs."""
    logs = (
        db.query(InteractionLog)
        .order_by(InteractionLog.created_at.desc())
        .limit(50)
        .all()
    )
    items = [
        LogEntry(
            id=entry.id,
            created_at=entry.created_at,
            request_text=entry.request_text,
            response_text=entry.response_text,
            model=entry.model,
            user_id=entry.user_id,
            risk_score=entry.risk_score,
            severity=entry.severity,
            labels=entry.labels,
        )
        for entry in logs
    ]
    return LogsResponse(request_id=request.state.request_id, items=items)
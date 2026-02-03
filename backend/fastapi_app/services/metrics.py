from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.fastapi_app.db.models import InteractionLog
from backend.fastapi_app.schemas import MonitorRequest, ReportSummary
from backend.fastapi_app.services.detector import RiskResult


def normalize_severity(score: float) -> str:
    """Map a numeric risk score to a severity bucket."""
    if score >= 0.9:
        return "critical"
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    if score >= 0.2:
        return "low"
    return "info"


def log_interaction(
    db: Session,
    payload: MonitorRequest,
    risk: RiskResult,
    severity: str,
) -> str:
    """Persist a monitored interaction and return the log ID."""
    entry = InteractionLog(
        request_text=payload.request_text,
        response_text=payload.response_text,
        model=payload.model,
        user_id=payload.user_id,
        risk_score=risk.score,
        severity=severity,
        labels=risk.labels,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry.id


def build_summary_report(db: Session, request_id: str = "unknown") -> ReportSummary:
    """Aggregate governance metrics for reporting."""
    total, avg_score = db.query(
        func.count(InteractionLog.id),
        func.avg(InteractionLog.risk_score),
    ).first()

    high_risk = db.query(InteractionLog).filter(InteractionLog.risk_score >= 0.7).count()
    return ReportSummary(
        total_interactions=total or 0,
        avg_risk_score=float(avg_score or 0.0),
        high_risk_count=high_risk,
        last_updated=datetime.utcnow(),
        request_id=request_id,
    )

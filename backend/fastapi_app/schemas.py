from datetime import datetime

from pydantic import BaseModel, Field


class MonitorRequest(BaseModel):
    request_text: str = Field(..., min_length=1)
    response_text: str = Field(..., min_length=1)
    model: str | None = None
    user_id: str | None = None


class MonitorResponse(BaseModel):
    log_id: str
    risk_score: float
    labels: list[str]
    severity: str
    alert_sent: bool
    request_id: str


class LogEntry(BaseModel):
    id: str
    created_at: datetime
    request_text: str
    response_text: str
    model: str | None
    user_id: str | None
    risk_score: float
    severity: str
    labels: list[str]


class LogsResponse(BaseModel):
    request_id: str
    items: list[LogEntry]


class ReportSummary(BaseModel):
    total_interactions: int
    avg_risk_score: float
    high_risk_count: int
    last_updated: datetime
    request_id: str


class HealthResponse(BaseModel):
    status: str
    request_id: str
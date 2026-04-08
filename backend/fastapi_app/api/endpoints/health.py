from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.fastapi_app.db.session import get_db
from backend.fastapi_app.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check(request: Request) -> HealthResponse:
    """Liveness: process is up (use for load balancers that only need a heartbeat)."""
    return HealthResponse(status="ok", request_id=request.state.request_id)


@router.get("/health/ready", response_model=HealthResponse)
def readiness(request: Request, db: Session = Depends(get_db)) -> HealthResponse:
    """Readiness: database is reachable (use before receiving traffic)."""
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database_unavailable") from exc
    return HealthResponse(status="ok", request_id=request.state.request_id)

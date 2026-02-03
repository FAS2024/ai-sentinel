from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from backend.fastapi_app.db.session import get_db
from backend.fastapi_app.schemas import ReportSummary
from backend.fastapi_app.services.metrics import build_summary_report

router = APIRouter()


@router.get("/reports/summary", response_model=ReportSummary)
def get_summary(request: Request, db: Session = Depends(get_db)) -> ReportSummary:
    """Return aggregate governance metrics for recent interactions."""
    return build_summary_report(db, request_id=request.state.request_id)

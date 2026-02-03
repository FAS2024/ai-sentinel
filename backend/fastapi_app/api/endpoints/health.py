from fastapi import APIRouter, Request

from backend.fastapi_app.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check(request: Request) -> HealthResponse:
    """Lightweight health check for uptime monitoring."""
    return HealthResponse(status="ok", request_id=request.state.request_id)

from fastapi import APIRouter

from backend.fastapi_app.api.endpoints.health import router as health_router
from backend.fastapi_app.api.endpoints.monitor import router as monitor_router
from backend.fastapi_app.api.endpoints.reports import router as reports_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(monitor_router, tags=["monitoring"])
api_router.include_router(reports_router, tags=["reports"])

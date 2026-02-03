import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.fastapi_app.api.router import api_router
from backend.fastapi_app.core.config import settings
from backend.fastapi_app.core.logging import configure_logging
from backend.fastapi_app.db import models  # noqa: F401
from backend.fastapi_app.db.session import Base, engine

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    configure_logging()
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(api_router, prefix="/v1")

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "request_complete method=%s path=%s status=%s duration_ms=%.2f request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request_id,
        )
        return response

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.warning(
            "http_error status=%s detail=%s request_id=%s", exc.status_code, exc.detail, request_id
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "request_id": request_id},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.exception("unhandled_error request_id=%s", request_id)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "request_id": request_id},
        )

    @app.get("/")
    async def root():
        return {"status": "ok", "service": settings.app_name, "docs": "/docs"}

    return app


app = create_app()

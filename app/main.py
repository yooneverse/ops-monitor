import asyncio
import logging
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.api.dashboard import router as dashboard_router
from app.security import get_allowed_hosts, is_docs_enabled, require_monitor_auth
from app.services.db_check import check_database_connection
from app.services.monitoring_loop import is_monitoring_enabled, monitor_services
from app.services.runtime_logs import configure_runtime_logging
from app.services.system_check import check_system_status

configure_runtime_logging()
logger = logging.getLogger("uvicorn.error")
monitoring_task = None


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def build_readiness_response(database_status: dict) -> tuple[dict, int]:
    is_ready = database_status.get("status") == "connected"

    payload = {
        "status": "ready" if is_ready else "not_ready",
        "timestamp": now_iso(),
    }

    return payload, 200 if is_ready else 503


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ops Monitor",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    app.include_router(
        dashboard_router,
        dependencies=[Depends(require_monitor_auth)],
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=get_allowed_hosts())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://127.0.0.1"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return {
            "message": "Ops Monitor API is running",
        }

    @app.get("/livez")
    def liveness_check():
        return {
            "status": "ok",
            "timestamp": now_iso(),
        }

    @app.get("/readyz")
    def readiness_check():
        database_status = check_database_connection()
        payload, status_code = build_readiness_response(database_status)

        if status_code >= 500:
            logger.warning("Readiness check completed with errors")
            return JSONResponse(status_code=status_code, content=payload)

        logger.info("Readiness check completed successfully")
        return payload

    @app.get("/health", dependencies=[Depends(require_monitor_auth)])
    def health_check():
        database_status = check_database_connection()
        status = database_status.get("status")

        if status in {"disconnected", "error"}:
            logger.info("Health check completed with errors")
        else:
            logger.info("Health check completed successfully")

        return {
            "api": "ok",
            "database": database_status,
            "timestamp": now_iso(),
        }

    @app.get("/system", dependencies=[Depends(require_monitor_auth)])
    def system_status():
        return check_system_status()

    if is_docs_enabled():
        @app.get("/openapi.json", include_in_schema=False, dependencies=[Depends(require_monitor_auth)])
        def openapi_schema():
            return get_openapi(
                title=app.title,
                version="1.0.0",
                routes=app.routes,
            )

        @app.get("/docs", include_in_schema=False, dependencies=[Depends(require_monitor_auth)])
        def swagger_ui():
            return get_swagger_ui_html(
                openapi_url="/openapi.json",
                title=f"{app.title} - Swagger UI",
            )

    @app.on_event("startup")
    async def startup_event():
        global monitoring_task

        if not is_monitoring_enabled():
            logger.info("Monitoring startup skipped")
            monitoring_task = None
            return

        monitoring_task = asyncio.create_task(monitor_services())

    @app.on_event("shutdown")
    async def shutdown_event():
        global monitoring_task

        if monitoring_task:
            monitoring_task.cancel()

            try:
                await monitoring_task
            except asyncio.CancelledError:
                pass

    return app


app = create_app()

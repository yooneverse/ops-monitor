from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from app.api.dashboard_page import get_dashboard_html
from app.security import require_monitor_auth
from app.services.alert_history import get_alert_history
from app.services.admin_actions import restart_database_service
from app.services.monitoring_loop import get_monitoring_status

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    return get_dashboard_html()


@router.get("/alerts")
def get_alerts() -> list[dict]:
    return get_alert_history()


@router.get("/monitoring/status")
def monitoring_status() -> dict:
    return get_monitoring_status()


@router.post("/admin/database/restart", response_model=None)
def restart_database(username: str = Depends(require_monitor_auth)):
    result = restart_database_service(requested_by=username)

    if result["status"] != "ok":
        return JSONResponse(status_code=503, content=result)

    return result

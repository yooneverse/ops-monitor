from fastapi import Depends
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from app.api.dashboard_page import get_dashboard_html
from app.security import require_monitor_auth
from app.services.alert_history import get_alert_history
from app.services.admin_actions import restart_database_service
from app.services.dashboard_workspace import build_dashboard_workspace
from app.services.dashboard_workspace import confirm_dashboard_report
from app.services.monitoring_loop import get_monitoring_status

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    return get_dashboard_html()


@router.get("/alerts")
def get_alerts() -> list[dict]:
    return get_alert_history()


@router.get("/dashboard/workspace")
def dashboard_workspace() -> dict:
    return build_dashboard_workspace()


@router.get("/monitoring/status")
def monitoring_status() -> dict:
    return get_monitoring_status()


@router.post("/dashboard/reports/{report_id}/confirm")
def confirm_report(
    report_id: str,
    username: str = Depends(require_monitor_auth),
) -> dict:
    try:
        return confirm_dashboard_report(
            report_id=report_id,
            confirmed_by=username,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/admin/database/restart", response_model=None)
def restart_database(
    username: str = Depends(require_monitor_auth),
):
    result = restart_database_service(requested_by=username)

    if result["status"] != "ok":
        return JSONResponse(status_code=503, content=result)

    return result

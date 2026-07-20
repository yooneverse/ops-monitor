from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.api.dashboard_page import get_dashboard_html
from app.services.alert_history import get_alert_history
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

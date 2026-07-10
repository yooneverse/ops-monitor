import logging
from typing import Optional

from app.services.runtime_logs import persist_alert_event

MAX_ALERT_HISTORY = 20
logger = logging.getLogger("uvicorn.error")

alert_history: list[dict] = []


def add_alert_history(event: dict) -> None:
    alert_history.insert(0, event)

    try:
        persist_alert_event(event)
    except OSError:
        logger.exception("Failed to persist alert event")

    if len(alert_history) > MAX_ALERT_HISTORY:
        alert_history.pop()


def get_alert_history() -> list[dict]:
    return alert_history


def get_latest_alert() -> Optional[dict]:
    if not alert_history:
        return None

    return alert_history[0]

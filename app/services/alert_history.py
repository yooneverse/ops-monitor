from typing import Optional

MAX_ALERT_HISTORY = 20

alert_history: list[dict] = []


def add_alert_history(event: dict) -> None:
    alert_history.insert(0, event)

    if len(alert_history) > MAX_ALERT_HISTORY:
        alert_history.pop()


def get_alert_history() -> list[dict]:
    return alert_history


def get_latest_alert() -> Optional[dict]:
    if not alert_history:
        return None

    return alert_history[0]
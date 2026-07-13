import asyncio
import logging
from datetime import datetime

from app.config import get_settings
from app.services.alert_history import add_alert_history
from app.services.db_check import check_database_connection
from app.services.discord_webhook import send_discord_alert
from app.services.system_check import check_system_status

logger = logging.getLogger("uvicorn.error")

previous_state = {
    "db_status": None,
    "memory_alert": False,
    "disk_alert": False,
}

monitoring_status = {
    "enabled": False,
    "interval_seconds": 60,
    "discord_webhook_configured": False,
    "last_check": None,
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def get_monitor_interval() -> int:
    return get_settings().monitor_interval_seconds


def is_monitoring_enabled() -> bool:
    return get_settings().monitoring_enabled


def get_threshold(name: str, default: int) -> int:
    settings = get_settings()

    if name == "MEMORY_ALERT_THRESHOLD":
        return settings.memory_alert_threshold

    if name == "DISK_ALERT_THRESHOLD":
        return settings.disk_alert_threshold

    return default


def refresh_monitoring_status() -> None:
    settings = get_settings()
    monitoring_status["enabled"] = is_monitoring_enabled()
    monitoring_status["interval_seconds"] = get_monitor_interval()
    monitoring_status["discord_webhook_configured"] = bool(settings.discord_webhook_url)


def build_alert_event(
    event_type: str,
    target: str,
    status: str,
    message: str,
) -> dict:
    return {
        "type": event_type,
        "target": target,
        "status": status,
        "message": message,
        "timestamp": now_iso(),
    }


def evaluate_db_transition(current_db_status: str) -> dict | None:
    previous_db_status = previous_state.get("db_status")

    if previous_db_status is None:
        previous_state["db_status"] = current_db_status

        if current_db_status == "disconnected":
            return build_alert_event(
                event_type="incident",
                target="database",
                status="disconnected",
                message="Database connection failed",
            )

        return None

    if previous_db_status == current_db_status:
        return None

    previous_state["db_status"] = current_db_status

    if previous_db_status == "connected" and current_db_status == "disconnected":
        return build_alert_event(
            event_type="incident",
            target="database",
            status="disconnected",
            message="Database connection failed",
        )

    if previous_db_status == "disconnected" and current_db_status == "connected":
        return build_alert_event(
            event_type="recovery",
            target="database",
            status="connected",
            message="Database connection recovered",
        )

    return None


def evaluate_resource_thresholds(system_status: dict) -> list[dict]:
    events = []

    memory_threshold = get_threshold("MEMORY_ALERT_THRESHOLD", 80)
    disk_threshold = get_threshold("DISK_ALERT_THRESHOLD", 80)

    memory_percent = system_status.get("memory", {}).get("percent", 0)
    disk_percent = system_status.get("disk", {}).get("percent", 0)

    current_memory_alert = memory_percent >= memory_threshold
    current_disk_alert = disk_percent >= disk_threshold

    if not previous_state["memory_alert"] and current_memory_alert:
        events.append(
            build_alert_event(
                event_type="resource_alert",
                target="memory",
                status="warning",
                message=f"Memory usage exceeded threshold: {memory_percent}%",
            )
        )

    if previous_state["memory_alert"] and not current_memory_alert:
        events.append(
            build_alert_event(
                event_type="resource_recovery",
                target="memory",
                status="normal",
                message=f"Memory usage recovered: {memory_percent}%",
            )
        )

    if not previous_state["disk_alert"] and current_disk_alert:
        events.append(
            build_alert_event(
                event_type="resource_alert",
                target="disk",
                status="warning",
                message=f"Disk usage exceeded threshold: {disk_percent}%",
            )
        )

    if previous_state["disk_alert"] and not current_disk_alert:
        events.append(
            build_alert_event(
                event_type="resource_recovery",
                target="disk",
                status="normal",
                message=f"Disk usage recovered: {disk_percent}%",
            )
        )

    previous_state["memory_alert"] = current_memory_alert
    previous_state["disk_alert"] = current_disk_alert

    return events


def notify_event(event: dict) -> None:
    add_alert_history(event)

    level = "info"

    if event["type"] == "incident":
        level = "critical"
    elif event["type"] == "recovery":
        level = "recovery"
    elif event["type"] == "resource_alert":
        level = "warning"
    elif event["type"] == "resource_recovery":
        level = "recovery"

    sent = send_discord_alert(
        title=event["message"],
        fields={
            "Type": event["type"],
            "Target": event["target"],
            "Status": event["status"],
            "Time": event["timestamp"],
        },
        level=level,
    )

    if not sent and event["target"] != "discord_webhook":
        add_alert_history(
            build_alert_event(
                event_type="notification_error",
                target="discord_webhook",
                status="failed",
                message="Discord webhook send failed",
            )
        )


async def check_and_notify() -> None:
    refresh_monitoring_status()

    db_status = check_database_connection()
    system_status = check_system_status()

    monitoring_status["last_check"] = now_iso()

    db_event = evaluate_db_transition(db_status.get("status"))

    if db_event:
        notify_event(db_event)

    resource_events = evaluate_resource_thresholds(system_status)

    for event in resource_events:
        notify_event(event)

    logger.info(
        "Monitoring cycle completed: db=%s memory=%s%% disk=%s%%",
        db_status.get("status"),
        system_status.get("memory", {}).get("percent", 0),
        system_status.get("disk", {}).get("percent", 0),
    )


async def monitor_services() -> None:
    refresh_monitoring_status()

    if not monitoring_status["enabled"]:
        logger.info("Monitoring loop is disabled by configuration")
        return

    logger.info("Monitoring loop started")

    while True:
        try:
            await check_and_notify()

        except Exception as error:
            logger.exception("Monitoring loop failed")
            event = build_alert_event(
                event_type="monitoring_error",
                target="monitoring_loop",
                status="error",
                message=str(error),
            )
            add_alert_history(event)

        await asyncio.sleep(get_monitor_interval())


def get_monitoring_status() -> dict:
    refresh_monitoring_status()
    return monitoring_status

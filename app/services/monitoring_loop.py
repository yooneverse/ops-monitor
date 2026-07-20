import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime

from app.config import Settings, get_settings
from app.services.alert_history import add_alert_history
from app.services.db_check import check_database_connection
from app.services.discord_webhook import send_discord_alert
from app.services.system_check import check_system_status

logger = logging.getLogger("uvicorn.error")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class MonitoringStatusView:
    enabled: bool = False
    interval_seconds: int = 30
    discord_webhook_configured: bool = False
    monitor_auth_configured: bool = False
    api_docs_enabled: bool = False
    thresholds: dict[str, int] = field(
        default_factory=lambda: {
            "memory_percent": 80,
            "disk_percent": 80,
        }
    )
    config_warnings: list[str] = field(default_factory=list)
    last_check: str | None = None

    def refresh_from_settings(self, settings: Settings) -> None:
        self.enabled = settings.monitoring_enabled
        self.interval_seconds = settings.monitor_interval_seconds
        self.discord_webhook_configured = bool(settings.discord_webhook_url)
        self.monitor_auth_configured = settings.monitor_auth_configured
        self.api_docs_enabled = settings.api_docs_enabled
        self.thresholds = {
            "memory_percent": settings.memory_alert_threshold,
            "disk_percent": settings.disk_alert_threshold,
        }
        self.config_warnings = list(settings.config_warnings)

    def to_dict(self) -> dict:
        return {
            "enabled": self.enabled,
            "interval_seconds": self.interval_seconds,
            "discord_webhook_configured": self.discord_webhook_configured,
            "monitor_auth_configured": self.monitor_auth_configured,
            "api_docs_enabled": self.api_docs_enabled,
            "thresholds": dict(self.thresholds),
            "config_warnings": list(self.config_warnings),
            "last_check": self.last_check,
        }


@dataclass
class MonitoringRuntimeState:
    previous_db_status: str | None = None
    memory_alert_active: bool = False
    disk_alert_active: bool = False
    status_view: MonitoringStatusView = field(default_factory=MonitoringStatusView)

    def refresh_status(self, settings: Settings) -> None:
        self.status_view.refresh_from_settings(settings)

    def mark_last_check(self) -> None:
        self.status_view.last_check = now_iso()

    def evaluate_db_transition(self, current_db_status: str | None) -> dict | None:
        if current_db_status is None:
            return None

        previous_db_status = self.previous_db_status

        if previous_db_status is None:
            self.previous_db_status = current_db_status

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

        self.previous_db_status = current_db_status

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

    def evaluate_resource_thresholds(
        self,
        system_status: dict,
        settings: Settings,
    ) -> list[dict]:
        events = []
        memory_threshold = settings.memory_alert_threshold
        disk_threshold = settings.disk_alert_threshold

        memory_percent = system_status.get("memory", {}).get("percent", 0)
        disk_percent = system_status.get("disk", {}).get("percent", 0)

        current_memory_alert = memory_percent >= memory_threshold
        current_disk_alert = disk_percent >= disk_threshold

        if not self.memory_alert_active and current_memory_alert:
            events.append(
                build_alert_event(
                    event_type="resource_alert",
                    target="memory",
                    status="warning",
                    message=f"Memory usage exceeded threshold: {memory_percent}%",
                )
            )

        if self.memory_alert_active and not current_memory_alert:
            events.append(
                build_alert_event(
                    event_type="resource_recovery",
                    target="memory",
                    status="normal",
                    message=f"Memory usage recovered: {memory_percent}%",
                )
            )

        if not self.disk_alert_active and current_disk_alert:
            events.append(
                build_alert_event(
                    event_type="resource_alert",
                    target="disk",
                    status="warning",
                    message=f"Disk usage exceeded threshold: {disk_percent}%",
                )
            )

        if self.disk_alert_active and not current_disk_alert:
            events.append(
                build_alert_event(
                    event_type="resource_recovery",
                    target="disk",
                    status="normal",
                    message=f"Disk usage recovered: {disk_percent}%",
                )
            )

        self.memory_alert_active = current_memory_alert
        self.disk_alert_active = current_disk_alert
        return events

    def reset(self) -> None:
        self.previous_db_status = None
        self.memory_alert_active = False
        self.disk_alert_active = False
        self.status_view = MonitoringStatusView()


runtime_state = MonitoringRuntimeState()


def reset_monitoring_state() -> None:
    runtime_state.reset()


def get_monitor_interval() -> int:
    return get_settings().monitor_interval_seconds


def is_monitoring_enabled() -> bool:
    return get_settings().monitoring_enabled


def refresh_monitoring_status() -> None:
    runtime_state.refresh_status(get_settings())


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
    settings = get_settings()
    runtime_state.refresh_status(settings)

    db_status = check_database_connection()
    system_status = check_system_status()

    runtime_state.mark_last_check()

    db_event = runtime_state.evaluate_db_transition(db_status.get("status"))

    if db_event:
        notify_event(db_event)

    resource_events = runtime_state.evaluate_resource_thresholds(
        system_status,
        settings,
    )

    for event in resource_events:
        notify_event(event)

    logger.info(
        "Monitoring cycle completed: db=%s memory=%s%% disk=%s%%",
        db_status.get("status"),
        system_status.get("memory", {}).get("percent", 0),
        system_status.get("disk", {}).get("percent", 0),
    )


async def monitor_services() -> None:
    settings = get_settings()
    runtime_state.refresh_status(settings)

    if not runtime_state.status_view.enabled:
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
    runtime_state.refresh_status(get_settings())
    return runtime_state.status_view.to_dict()

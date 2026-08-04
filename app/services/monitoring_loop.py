import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime

from app.config import Settings, get_settings
from app.services.alert_history import add_alert_history
from app.services.discord_webhook import send_discord_alert
from app.services.monitoring_targets import (
    ServiceCheckTarget,
    collect_service_statuses,
    select_service_check_targets,
)
from app.services.runtime_logs import persist_monitoring_run
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
    active_targets: list[str] = field(default_factory=list)
    excluded_targets: list[str] = field(default_factory=list)
    target_warnings: list[str] = field(default_factory=list)
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
        self.excluded_targets = list(settings.monitoring_excluded_targets)
        self.active_targets = []
        self.target_warnings = []

    def apply_target_metadata(
        self,
        active_targets: list[str],
        target_warnings: list[str],
    ) -> None:
        self.active_targets = active_targets
        self.target_warnings = target_warnings

    def to_dict(self) -> dict:
        return {
            "enabled": self.enabled,
            "interval_seconds": self.interval_seconds,
            "discord_webhook_configured": self.discord_webhook_configured,
            "monitor_auth_configured": self.monitor_auth_configured,
            "api_docs_enabled": self.api_docs_enabled,
            "thresholds": dict(self.thresholds),
            "config_warnings": list(self.config_warnings),
            "active_targets": list(self.active_targets),
            "excluded_targets": list(self.excluded_targets),
            "target_warnings": list(self.target_warnings),
            "last_check": self.last_check,
        }


@dataclass
class MonitoringRuntimeState:
    previous_service_statuses: dict[str, str | None] = field(default_factory=dict)
    memory_alert_active: bool = False
    disk_alert_active: bool = False
    status_view: MonitoringStatusView = field(default_factory=MonitoringStatusView)

    def refresh_status(self, settings: Settings) -> None:
        self.status_view.refresh_from_settings(settings)

    def mark_last_check(self) -> None:
        self.status_view.last_check = now_iso()

    def apply_target_metadata(
        self,
        active_targets: list[str],
        target_warnings: list[str],
    ) -> None:
        self.status_view.apply_target_metadata(active_targets, target_warnings)

    def evaluate_service_transition(
        self,
        target: ServiceCheckTarget,
        current_status: str | None,
    ) -> dict | None:
        if current_status is None or current_status in target.ignored_statuses:
            return None

        previous_status = self.previous_service_statuses.get(target.key)

        if previous_status is None:
            self.previous_service_statuses[target.key] = current_status

            if current_status != target.expected_status:
                return build_alert_event(
                    event_type="incident",
                    target=target.key,
                    status=current_status,
                    message=target.unavailable_message,
                )

            return None

        if previous_status == current_status:
            return None

        self.previous_service_statuses[target.key] = current_status

        if previous_status == target.expected_status and current_status != target.expected_status:
            return build_alert_event(
                event_type="incident",
                target=target.key,
                status=current_status,
                message=target.unavailable_message,
            )

        if previous_status != target.expected_status and current_status == target.expected_status:
            return build_alert_event(
                event_type="recovery",
                target=target.key,
                status=current_status,
                message=target.recovery_message,
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
        self.previous_service_statuses = {}
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


def build_monitoring_run_report(
    *,
    started_at: str,
    completed_at: str,
    active_targets: tuple[ServiceCheckTarget, ...],
    excluded_targets: tuple[str, ...],
    service_statuses: dict[str, dict],
    system_status: dict,
    events: list[dict],
    target_warnings: list[str],
) -> dict:
    overall_status = "ok"

    if target_warnings:
        overall_status = "warning"

    if events and any(event["type"] in {"incident", "resource_alert", "monitoring_error"} for event in events):
        overall_status = "warning"

    return {
        "run_id": completed_at.replace("-", "").replace(":", "").replace("T", "-"),
        "started_at": started_at,
        "completed_at": completed_at,
        "overall_status": overall_status,
        "active_targets": [target.key for target in active_targets],
        "excluded_targets": list(excluded_targets),
        "target_warnings": list(target_warnings),
        "service_statuses": service_statuses,
        "system_status": {
            "memory_percent": system_status.get("memory", {}).get("percent", 0),
            "disk_percent": system_status.get("disk", {}).get("percent", 0),
        },
        "events": list(events),
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

    run_started_at = now_iso()
    service_targets, target_warnings = select_service_check_targets(
        settings.monitoring_excluded_targets
    )
    runtime_state.apply_target_metadata(
        active_targets=[target.key for target in service_targets],
        target_warnings=target_warnings,
    )
    service_statuses = collect_service_statuses(service_targets)
    system_status = check_system_status()
    generated_events: list[dict] = []

    runtime_state.mark_last_check()

    for target in service_targets:
        target_status = service_statuses.get(target.key, {}).get("status")
        target_event = runtime_state.evaluate_service_transition(target, target_status)

        if target_event:
            notify_event(target_event)
            generated_events.append(target_event)

    resource_events = runtime_state.evaluate_resource_thresholds(
        system_status,
        settings,
    )

    for event in resource_events:
        notify_event(event)
        generated_events.append(event)

    run_completed_at = now_iso()
    persist_monitoring_run(
        build_monitoring_run_report(
            started_at=run_started_at,
            completed_at=run_completed_at,
            active_targets=service_targets,
            excluded_targets=settings.monitoring_excluded_targets,
            service_statuses=service_statuses,
            system_status=system_status,
            events=generated_events,
            target_warnings=target_warnings,
        )
    )

    logger.info(
        "Monitoring cycle completed: db=%s demo_notes=%s memory=%s%% disk=%s%%",
        service_statuses.get("database", {}).get("status"),
        service_statuses.get("demo_notes", {}).get("status"),
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

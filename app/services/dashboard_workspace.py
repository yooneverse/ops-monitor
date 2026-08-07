import hashlib
import json
from datetime import datetime
from pathlib import Path
from threading import Lock

from app.services.alert_history import get_alert_history
from app.services.db_check import check_database_connection
from app.services.demo_notes_check import check_demo_notes_service
from app.services.monitoring_loop import get_monitoring_status
from app.services.runtime_logs import get_log_dir
from app.services.system_check import check_system_status

_confirmation_lock = Lock()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def get_report_confirmation_path() -> Path:
    return get_log_dir() / "dashboard" / "report-confirmations.json"


def load_report_confirmations() -> dict[str, dict[str, str]]:
    path = get_report_confirmation_path()

    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_report_confirmations(store: dict[str, dict[str, str]]) -> None:
    path = get_report_confirmation_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with _confirmation_lock:
        path.write_text(
            json.dumps(store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def build_health_snapshot() -> dict:
    return {
        "api": "ok",
        "database": check_database_connection(),
        "demo_notes": check_demo_notes_service(),
        "timestamp": now_iso(),
    }


def build_report_signature(report: dict) -> str:
    signature_source = json.dumps(
        {
            "report_id": report["report_id"],
            "priority": report["priority"],
            "title": report["title"],
            "summary": report["summary"],
            "facts": report["facts"],
            "recommended_actions": report["recommended_actions"],
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha1(signature_source.encode("utf-8")).hexdigest()


def apply_confirmation_state(reports: list[dict]) -> list[dict]:
    confirmations = load_report_confirmations()
    resolved_reports: list[dict] = []

    for report in reports:
        signature = build_report_signature(report)
        stored_confirmation = confirmations.get(report["report_id"])
        is_confirmed = bool(
            stored_confirmation
            and stored_confirmation.get("signature") == signature
        )

        resolved_reports.append(
            {
                **report,
                "confirmed": is_confirmed,
                "confirmed_at": stored_confirmation.get("confirmed_at")
                if is_confirmed
                else None,
                "confirmed_by": stored_confirmation.get("confirmed_by")
                if is_confirmed
                else None,
            }
        )

    return resolved_reports


def build_analysis_reports(
    health: dict,
    system_status: dict,
    monitoring: dict,
    alerts: list[dict],
) -> list[dict]:
    reports: list[dict] = []

    database_status = health.get("database", {}).get("status")
    demo_notes_status = health.get("demo_notes", {}).get("status")
    memory_percent = system_status.get("memory", {}).get("percent", 0)
    disk_percent = system_status.get("disk", {}).get("percent", 0)
    memory_threshold = monitoring.get("thresholds", {}).get("memory_percent", 80)
    disk_threshold = monitoring.get("thresholds", {}).get("disk_percent", 80)

    if database_status != "connected" or demo_notes_status == "disconnected":
        facts = []

        if database_status != "connected":
            facts.append("데이터베이스 연결이 현재 정상 상태가 아닙니다.")

        if demo_notes_status == "disconnected":
            facts.append("부가 서비스 demo-notes 연결이 끊긴 상태입니다.")

        reports.append(
            {
                "report_id": "service-availability",
                "category": "availability",
                "priority": "critical",
                "title": "서비스 가용성 분석 보고서",
                "headline": "핵심 서비스 연결 상태를 우선 확인해야 합니다.",
                "summary": "API가 살아 있어도 저장소나 부가 서비스 연결이 끊기면 운영자는 즉시 영향 범위를 판단해야 합니다.",
                "facts": facts,
                "recommended_actions": [
                    "장애 대상의 최근 알림 타임라인을 먼저 확인합니다.",
                    "DB 또는 부가 서비스 복구 이후 recovery 이벤트가 남는지 재확인합니다.",
                    "필요하면 운영 액션 영역에서 보호된 조치를 수행합니다.",
                ],
                "owner": "WEB/WAS 운영",
            }
        )

    config_warnings = list(monitoring.get("config_warnings", []))
    if config_warnings:
        reports.append(
            {
                "report_id": "runtime-configuration",
                "category": "configuration",
                "priority": "high",
                "title": "런타임 설정 검토 보고서",
                "headline": "현재 설정 상태는 서비스 운영은 가능하지만 보완이 필요합니다.",
                "summary": "운영 설정은 단발성 경고가 아니라 반복 점검과 복기 품질에 직접 영향을 줍니다.",
                "facts": config_warnings,
                "recommended_actions": [
                    "경고 항목을 .env 기준으로 하나씩 정리합니다.",
                    "임계치와 모니터링 주기가 실제 운영 의도와 맞는지 재확인합니다.",
                    "변경 후 대시보드와 /monitoring/status에서 경고가 사라졌는지 확인합니다.",
                ],
                "owner": "플랫폼 운영",
            }
        )

    recent_resource_events = [
        alert
        for alert in alerts
        if alert.get("type") in {"resource_alert", "resource_recovery"}
    ]
    resource_needs_attention = (
        memory_percent >= max(memory_threshold - 10, 1)
        or disk_percent >= max(disk_threshold - 10, 1)
        or bool(recent_resource_events)
    )

    if resource_needs_attention:
        reports.append(
            {
                "report_id": "capacity-watch",
                "category": "capacity",
                "priority": "medium",
                "title": "자원 추세 점검 보고서",
                "headline": "메모리 또는 디스크 사용량이 임계치 인접 구간에 들어왔습니다.",
                "summary": "즉시 장애가 아니더라도 임계치 근접 상태는 전조로 취급하고 추세를 보는 편이 안전합니다.",
                "facts": [
                    f"메모리 사용률 {memory_percent}% / 임계치 {memory_threshold}%",
                    f"디스크 사용률 {disk_percent}% / 임계치 {disk_threshold}%",
                    f"최근 자원 이벤트 {len(recent_resource_events)}건",
                ],
                "recommended_actions": [
                    "최근 자원 이벤트가 반복되는지 타임라인에서 확인합니다.",
                    "임계치 설정이 실제 운영 기준과 맞는지 검토합니다.",
                    "필요하면 로그 정리 또는 용량 증설 계획을 후속 작업으로 남깁니다.",
                ],
                "owner": "인프라 운영",
            }
        )

    notification_failures = [
        alert
        for alert in alerts
        if alert.get("type") == "notification_error"
    ]
    admin_actions = [
        alert
        for alert in alerts
        if alert.get("type") in {"admin_action", "admin_action_error"}
    ]

    if notification_failures or admin_actions:
        reports.append(
            {
                "report_id": "operations-audit",
                "category": "audit",
                "priority": "medium",
                "title": "운영 조치 및 알림 감사 보고서",
                "headline": "최근 운영 조치와 알림 전달 상태를 함께 복기할 필요가 있습니다.",
                "summary": "운영 사이트에서는 상태 자체보다 누가 어떤 조치를 했고, 그 결과가 어떻게 남았는지가 중요합니다.",
                "facts": [
                    f"최근 운영 액션 {len(admin_actions)}건",
                    f"최근 알림 전송 실패 {len(notification_failures)}건",
                ],
                "recommended_actions": [
                    "운영 액션 이력에서 성공/실패와 메시지를 확인합니다.",
                    "알림 실패가 있었다면 Discord 웹훅 설정과 네트워크 상태를 재확인합니다.",
                    "필요한 후속 조치를 운영 메모나 티켓으로 연결합니다.",
                ],
                "owner": "운영 리드",
            }
        )

    if not reports:
        reports.append(
            {
                "report_id": "daily-stability-brief",
                "category": "briefing",
                "priority": "low",
                "title": "일일 운영 브리핑",
                "headline": "현재 기준으로 즉시 대응이 필요한 이슈는 보이지 않습니다.",
                "summary": "운영 상태가 안정적일 때도 마지막 점검 시각, 임계치, 알림 채널 상태를 함께 확인하는 흐름을 유지합니다.",
                "facts": [
                    "데이터베이스와 부가 서비스가 모두 연결 상태입니다.",
                    f"설정 경고 {len(config_warnings)}건",
                    f"최근 알림 {len(alerts)}건",
                ],
                "recommended_actions": [
                    "최근 타임라인에서 recovery 이후 반복 장애가 없는지 확인합니다.",
                    "다음 점검 주기 전까지 임계치와 알림 채널 상태를 유지합니다.",
                ],
                "owner": "운영 당번",
            }
        )

    return apply_confirmation_state(reports)


def build_service_board(health: dict, monitoring: dict) -> list[dict]:
    database_status = health.get("database", {}).get("status")
    demo_notes_status = health.get("demo_notes", {}).get("status")

    return [
        {
            "label": "API",
            "status": "정상" if health.get("api") == "ok" else "점검 필요",
            "tone": "ok" if health.get("api") == "ok" else "warning",
            "detail": "보호된 운영 API 응답 상태",
        },
        {
            "label": "Database",
            "status": "연결됨" if database_status == "connected" else "연결 안 됨",
            "tone": "ok" if database_status == "connected" else "critical",
            "detail": health.get("database", {}).get("message", "-"),
        },
        {
            "label": "Demo Notes",
            "status": "연결됨" if demo_notes_status == "connected" else "주의",
            "tone": "ok" if demo_notes_status == "connected" else "warning",
            "detail": health.get("demo_notes", {}).get("message", "-"),
        },
        {
            "label": "Monitoring Loop",
            "status": "실행 중" if monitoring.get("enabled") else "중지됨",
            "tone": "ok" if monitoring.get("enabled") else "warning",
            "detail": f"마지막 점검 {monitoring.get('last_check') or '-'}",
        },
    ]


def build_resource_board(system_status: dict, monitoring: dict) -> list[dict]:
    thresholds = monitoring.get("thresholds", {})
    memory_percent = system_status.get("memory", {}).get("percent", 0)
    disk_percent = system_status.get("disk", {}).get("percent", 0)
    memory_threshold = thresholds.get("memory_percent", 80)
    disk_threshold = thresholds.get("disk_percent", 80)

    return [
        {
            "label": "메모리",
            "value": f"{memory_percent}%",
            "tone": "warning" if memory_percent >= memory_threshold else "ok",
            "detail": f"{system_status.get('memory', {}).get('used_gb', 0)}GB / {system_status.get('memory', {}).get('total_gb', 0)}GB",
        },
        {
            "label": "디스크",
            "value": f"{disk_percent}%",
            "tone": "warning" if disk_percent >= disk_threshold else "ok",
            "detail": f"{system_status.get('disk', {}).get('used_gb', 0)}GB / {system_status.get('disk', {}).get('total_gb', 0)}GB",
        },
    ]


def build_timeline(alerts: list[dict], monitoring: dict) -> list[dict]:
    items: list[dict] = []

    if monitoring.get("last_check"):
        items.append(
            {
                "timestamp": monitoring["last_check"],
                "kind": "monitoring",
                "title": "모니터링 루프 마지막 점검",
                "summary": f"현재 주기 {monitoring.get('interval_seconds', 30)}초",
            }
        )

    for alert in alerts[:8]:
        items.append(
            {
                "timestamp": alert.get("timestamp", "-"),
                "kind": alert.get("type", "event"),
                "title": alert.get("message", "이벤트 메시지 없음"),
                "summary": f"{alert.get('target', '-')} / {alert.get('status', '-')}",
            }
        )

    return sorted(
        items,
        key=lambda item: item.get("timestamp", ""),
        reverse=True,
    )[:8]


def build_overview(
    reports: list[dict],
    alerts: list[dict],
    monitoring: dict,
) -> dict:
    pending_reports = [report for report in reports if not report["confirmed"]]
    confirmed_reports = [report for report in reports if report["confirmed"]]
    critical_reports = [
        report
        for report in pending_reports
        if report["priority"] == "critical"
    ]

    if critical_reports:
        operational_state = "critical"
        headline = "즉시 확인이 필요한 운영 보고서가 있습니다."
        summary = "가용성 또는 핵심 연결 상태와 관련된 분석 보고서가 확인 대기 중입니다."
    elif pending_reports:
        operational_state = "attention"
        headline = "운영 검토가 필요한 보고서가 남아 있습니다."
        summary = "현재 장애가 아니더라도 설정, 자원, 조치 이력을 검토할 항목이 있습니다."
    else:
        operational_state = "stable"
        headline = "모든 생성 보고서가 확인되었습니다."
        summary = "현재 운영 사이트 기준으로 미확인 분석 보고서는 없습니다."

    return {
        "operational_state": operational_state,
        "headline": headline,
        "summary": summary,
        "pending_reports": len(pending_reports),
        "confirmed_reports": len(confirmed_reports),
        "recent_alerts": len(alerts),
        "monitor_interval_seconds": monitoring.get("interval_seconds", 30),
    }


def build_dashboard_workspace() -> dict:
    health = build_health_snapshot()
    system_status = check_system_status()
    monitoring = get_monitoring_status()
    alerts = list(get_alert_history())
    reports = build_analysis_reports(health, system_status, monitoring, alerts)
    action_feed = [
        alert
        for alert in alerts
        if alert.get("type") in {"admin_action", "admin_action_error"}
    ][:5]

    return {
        "generated_at": now_iso(),
        "overview": build_overview(reports, alerts, monitoring),
        "health": health,
        "system": system_status,
        "monitoring": monitoring,
        "reports": reports,
        "service_board": build_service_board(health, monitoring),
        "resource_board": build_resource_board(system_status, monitoring),
        "timeline": build_timeline(alerts, monitoring),
        "config_warnings": list(monitoring.get("config_warnings", [])),
        "action_feed": action_feed,
        "alerts": alerts[:10],
    }


def confirm_dashboard_report(report_id: str, confirmed_by: str) -> dict:
    workspace = build_dashboard_workspace()
    matching_report = next(
        (report for report in workspace["reports"] if report["report_id"] == report_id),
        None,
    )

    if matching_report is None:
        raise ValueError(f"Unknown dashboard report: {report_id}")

    confirmations = load_report_confirmations()
    confirmations[report_id] = {
        "signature": build_report_signature(matching_report),
        "confirmed_at": now_iso(),
        "confirmed_by": confirmed_by,
    }
    save_report_confirmations(confirmations)

    refreshed_workspace = build_dashboard_workspace()
    confirmed_report = next(
        report
        for report in refreshed_workspace["reports"]
        if report["report_id"] == report_id
    )
    return confirmed_report

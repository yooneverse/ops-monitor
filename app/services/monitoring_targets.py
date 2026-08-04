from dataclasses import dataclass, field
from typing import Callable

from app.services.db_check import check_database_connection
from app.services.demo_notes_check import check_demo_notes_service


StatusChecker = Callable[[], dict]


@dataclass(frozen=True)
class ServiceCheckTarget:
    key: str
    checker: StatusChecker
    unavailable_message: str
    recovery_message: str
    expected_status: str = "connected"
    ignored_statuses: frozenset[str] = field(default_factory=frozenset)


SERVICE_CHECK_TARGETS: tuple[ServiceCheckTarget, ...] = (
    ServiceCheckTarget(
        key="database",
        checker=check_database_connection,
        unavailable_message="Database connection failed",
        recovery_message="Database connection recovered",
    ),
    ServiceCheckTarget(
        key="demo_notes",
        checker=check_demo_notes_service,
        unavailable_message="Demo notes service is unavailable",
        recovery_message="Demo notes service recovered",
        ignored_statuses=frozenset({"disabled"}),
    ),
)


def get_service_check_targets() -> tuple[ServiceCheckTarget, ...]:
    return SERVICE_CHECK_TARGETS


def select_service_check_targets(
    excluded_target_keys: tuple[str, ...] | None = None,
) -> tuple[tuple[ServiceCheckTarget, ...], list[str]]:
    excluded_keys = set(excluded_target_keys or ())
    known_keys = {target.key for target in SERVICE_CHECK_TARGETS}
    unknown_keys = sorted(excluded_keys - known_keys)

    warnings = [
        f"MONITORING_EXCLUDED_TARGETS에 알 수 없는 대상이 포함되어 무시되었습니다: {key}"
        for key in unknown_keys
    ]

    selected_targets = tuple(
        target
        for target in SERVICE_CHECK_TARGETS
        if target.key not in excluded_keys
    )

    if not selected_targets:
        warnings.append(
            "모든 체크 대상이 제외되어 서비스 상태 점검이 비활성화되었습니다."
        )

    return selected_targets, warnings


def collect_service_statuses(
    targets: tuple[ServiceCheckTarget, ...] | None = None,
) -> dict[str, dict]:
    selected_targets = targets or get_service_check_targets()
    return {
        target.key: target.checker()
        for target in selected_targets
    }

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


def collect_service_statuses(
    targets: tuple[ServiceCheckTarget, ...] | None = None,
) -> dict[str, dict]:
    selected_targets = targets or get_service_check_targets()
    return {
        target.key: target.checker()
        for target in selected_targets
    }

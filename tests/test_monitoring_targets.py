import unittest

from app.services.monitoring_loop import MonitoringRuntimeState
from app.services.monitoring_targets import (
    ServiceCheckTarget,
    collect_service_statuses,
)


class MonitoringTargetTests(unittest.TestCase):
    def test_collect_service_statuses_uses_registered_checker_results(self) -> None:
        targets = (
            ServiceCheckTarget(
                key="database",
                checker=lambda: {"status": "connected", "message": "ok"},
                unavailable_message="Database connection failed",
                recovery_message="Database connection recovered",
            ),
            ServiceCheckTarget(
                key="demo_notes",
                checker=lambda: {"status": "disabled", "message": "skipped"},
                unavailable_message="Demo notes service is unavailable",
                recovery_message="Demo notes service recovered",
                ignored_statuses=frozenset({"disabled"}),
            ),
        )

        statuses = collect_service_statuses(targets)

        self.assertEqual(statuses["database"]["status"], "connected")
        self.assertEqual(statuses["demo_notes"]["status"], "disabled")

    def test_service_transition_detects_incident_and_recovery_by_target_definition(self) -> None:
        runtime_state = MonitoringRuntimeState()
        target = ServiceCheckTarget(
            key="database",
            checker=lambda: {"status": "connected"},
            unavailable_message="Database connection failed",
            recovery_message="Database connection recovered",
        )

        self.assertIsNone(
            runtime_state.evaluate_service_transition(target, "connected")
        )

        incident_event = runtime_state.evaluate_service_transition(target, "disconnected")
        self.assertIsNotNone(incident_event)
        self.assertEqual(incident_event["type"], "incident")
        self.assertEqual(incident_event["target"], "database")

        recovery_event = runtime_state.evaluate_service_transition(target, "connected")
        self.assertIsNotNone(recovery_event)
        self.assertEqual(recovery_event["type"], "recovery")
        self.assertEqual(recovery_event["target"], "database")

    def test_service_transition_ignores_disabled_status_when_target_allows_it(self) -> None:
        runtime_state = MonitoringRuntimeState()
        target = ServiceCheckTarget(
            key="demo_notes",
            checker=lambda: {"status": "disabled"},
            unavailable_message="Demo notes service is unavailable",
            recovery_message="Demo notes service recovered",
            ignored_statuses=frozenset({"disabled"}),
        )

        self.assertIsNone(
            runtime_state.evaluate_service_transition(target, "disabled")
        )
        self.assertEqual(runtime_state.previous_service_statuses, {})


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

from fastapi.responses import JSONResponse

from app.api import dashboard
from app.api.dashboard_page import get_dashboard_html


class DashboardApiTests(unittest.TestCase):
    def test_dashboard_page_contains_expected_sections(self) -> None:
        html = dashboard.dashboard()

        self.assertIn("Ops Monitor 대시보드", html)
        self.assertIn("최근 알림", html)
        self.assertIn("설정 경고", html)
        self.assertIn("자동 갱신:", html)
        self.assertIn("loadDashboard()", html)
        self.assertIn("data-alert-filter", html)
        self.assertIn("sidebar-toggle", html)
        self.assertIn("menu-search", html)
        self.assertIn("data-nav-view", html)
        self.assertIn("db-restart-button", html)
        self.assertIn("db-status-signal", html)
        self.assertIn("점검 대상", html)
        self.assertIn("active-target-list", html)
        self.assertIn("excluded-target-list", html)
        self.assertIn("target-warning-list", html)
        self.assertIn("renderTargetMetadata", html)
        self.assertIn("최근 실행 리포트", html)
        self.assertIn("run-report-list", html)
        self.assertIn("renderRunReports", html)

    def test_dashboard_route_uses_shared_page_builder(self) -> None:
        self.assertEqual(dashboard.dashboard(), get_dashboard_html())

    def test_get_alerts_returns_service_data(self) -> None:
        alerts = [
            {
                "type": "incident",
                "target": "database",
                "status": "disconnected",
                "message": "Database connection failed",
                "timestamp": "2026-07-13T10:00:00",
            }
        ]

        with patch("app.api.dashboard.get_alert_history", return_value=alerts):
            self.assertEqual(dashboard.get_alerts(), alerts)

    def test_monitoring_status_returns_service_data(self) -> None:
        monitoring_status = {
            "enabled": True,
            "interval_seconds": 60,
            "discord_webhook_configured": False,
            "last_check": "2026-07-13T10:00:00",
        }

        with patch("app.api.dashboard.get_monitoring_status", return_value=monitoring_status):
            self.assertEqual(dashboard.monitoring_status(), monitoring_status)

    def test_recent_monitoring_runs_returns_runtime_log_data(self) -> None:
        run_reports = [
            {
                "run_id": "20260804-101500",
                "completed_at": "2026-08-04T10:15:02",
                "overall_status": "warning",
                "active_targets": ["database"],
                "excluded_targets": ["demo_notes"],
                "events": [{"type": "incident"}],
            }
        ]

        with patch("app.api.dashboard.read_recent_monitoring_runs", return_value=run_reports):
            self.assertEqual(dashboard.recent_monitoring_runs(), run_reports)

    def test_restart_database_returns_success_payload(self) -> None:
        payload = {
            "status": "ok",
            "message": "DB restarted",
            "requested_by": "ops-admin",
            "action": "restart_database",
            "timestamp": "2026-08-04T10:00:00",
        }

        with patch("app.api.dashboard.restart_database_service", return_value=payload):
            self.assertEqual(dashboard.restart_database(username="ops-admin"), payload)

    def test_restart_database_returns_503_response_on_failure(self) -> None:
        payload = {
            "status": "error",
            "message": "restart failed",
            "requested_by": "ops-admin",
            "action": "restart_database",
            "timestamp": "2026-08-04T10:00:00",
        }

        with patch("app.api.dashboard.restart_database_service", return_value=payload):
            response = dashboard.restart_database(username="ops-admin")

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()

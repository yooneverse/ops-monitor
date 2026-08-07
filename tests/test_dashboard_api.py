import unittest
from unittest.mock import patch

from fastapi.responses import JSONResponse

from app.api import dashboard
from app.api.dashboard_page import get_dashboard_html


class DashboardApiTests(unittest.TestCase):
    def test_dashboard_page_contains_expected_sections(self) -> None:
        html = dashboard.dashboard()

        self.assertIn("Ops Monitor 운영 워크스페이스", html)
        self.assertIn("운영 보고서 센터", html)
        self.assertIn("운영 보드", html)
        self.assertIn("운영 타임라인과 이벤트 로그", html)
        self.assertIn("loadWorkspace()", html)
        self.assertIn("sidebar-toggle", html)
        self.assertIn("menu-search", html)
        self.assertIn("data-nav-view", html)
        self.assertIn("db-restart-button", html)
        self.assertIn("confirm-report-button", html)
        self.assertIn("report-list", html)
        self.assertIn("report-detail", html)

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

    def test_dashboard_workspace_returns_aggregated_service_data(self) -> None:
        payload = {
            "generated_at": "2026-08-07T10:00:00",
            "overview": {"headline": "확인 필요"},
            "reports": [],
        }

        with patch("app.api.dashboard.build_dashboard_workspace", return_value=payload):
            self.assertEqual(dashboard.dashboard_workspace(), payload)

    def test_confirm_report_returns_confirmed_payload(self) -> None:
        payload = {
            "report_id": "service-availability",
            "confirmed": True,
            "confirmed_by": "ops-admin",
        }

        with patch("app.api.dashboard.confirm_dashboard_report", return_value=payload):
            self.assertEqual(
                dashboard.confirm_report("service-availability", username="ops-admin"),
                payload,
            )

    def test_restart_database_returns_success_payload(self) -> None:
        payload = {
            "status": "ok",
            "message": "DB restarted",
        }

        with patch("app.api.dashboard.restart_database_service", return_value=payload):
            self.assertEqual(dashboard.restart_database(), payload)

    def test_restart_database_returns_503_response_on_failure(self) -> None:
        payload = {
            "status": "error",
            "message": "restart failed",
        }

        with patch("app.api.dashboard.restart_database_service", return_value=payload):
            response = dashboard.restart_database()

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()

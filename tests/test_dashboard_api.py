import unittest
from unittest.mock import patch

from app.api import dashboard


class DashboardApiTests(unittest.TestCase):
    def test_dashboard_page_contains_expected_sections(self) -> None:
        html = dashboard.dashboard()

        self.assertIn("Ops Monitor Dashboard", html)
        self.assertIn("Recent Alerts", html)
        self.assertIn("Configuration Warnings", html)
        self.assertIn("Auto refresh every", html)
        self.assertIn("loadDashboard()", html)

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


if __name__ == "__main__":
    unittest.main()

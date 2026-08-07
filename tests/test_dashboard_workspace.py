import os
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app.config import reset_settings_cache
from app.services.dashboard_workspace import build_dashboard_workspace
from app.services.dashboard_workspace import confirm_dashboard_report


class DashboardWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_settings_cache()

    def tearDown(self) -> None:
        reset_settings_cache()

    def test_build_dashboard_workspace_includes_reports_and_boards(self) -> None:
        health = {
            "api": "ok",
            "database": {
                "status": "disconnected",
                "message": "Database connection failed",
            },
            "demo_notes": {
                "status": "connected",
                "message": "Demo notes service is available",
            },
            "timestamp": "2026-08-07T10:00:00",
        }
        system_status = {
            "memory": {"used_gb": 4.0, "total_gb": 8.0, "percent": 82},
            "disk": {"used_gb": 40.0, "total_gb": 100.0, "percent": 40},
        }
        monitoring_status = {
            "enabled": True,
            "interval_seconds": 45,
            "thresholds": {"memory_percent": 80, "disk_percent": 80},
            "config_warnings": ["MONITOR_INTERVAL_SECONDS must be greater than or equal to 5."],
            "last_check": "2026-08-07T09:58:00",
        }
        alerts = [
            {
                "type": "incident",
                "target": "database",
                "status": "disconnected",
                "message": "Database connection failed",
                "timestamp": "2026-08-07T09:57:00",
            }
        ]

        with patch("app.services.dashboard_workspace.build_health_snapshot", return_value=health), patch(
            "app.services.dashboard_workspace.check_system_status",
            return_value=system_status,
        ), patch(
            "app.services.dashboard_workspace.get_monitoring_status",
            return_value=monitoring_status,
        ), patch(
            "app.services.dashboard_workspace.get_alert_history",
            return_value=alerts,
        ):
            workspace = build_dashboard_workspace()

        self.assertEqual(workspace["overview"]["operational_state"], "critical")
        self.assertEqual(workspace["reports"][0]["report_id"], "service-availability")
        self.assertTrue(len(workspace["service_board"]) >= 4)
        self.assertEqual(workspace["timeline"][0]["timestamp"], "2026-08-07T09:58:00")

    def test_confirm_dashboard_report_persists_confirmation(self) -> None:
        workspace = {
            "reports": [
                {
                    "report_id": "daily-stability-brief",
                    "category": "briefing",
                    "priority": "low",
                    "title": "일일 운영 브리핑",
                    "headline": "안정 상태",
                    "summary": "안정 상태입니다.",
                    "facts": ["정상"],
                    "recommended_actions": ["계속 관찰"],
                    "owner": "운영 당번",
                    "confirmed": False,
                    "confirmed_at": None,
                    "confirmed_by": None,
                }
            ]
        }
        confirmed_workspace = {
            "reports": [
                {
                    **workspace["reports"][0],
                    "confirmed": True,
                    "confirmed_at": "2026-08-07T10:10:00",
                    "confirmed_by": "ops-admin",
                }
            ]
        }

        with TemporaryDirectory() as temp_dir:
            with patch.dict(os.environ, {"LOG_DIR": temp_dir}, clear=False):
                reset_settings_cache()
                with patch(
                    "app.services.dashboard_workspace.build_dashboard_workspace",
                    side_effect=[workspace, confirmed_workspace],
                ):
                    confirmed_report = confirm_dashboard_report(
                        report_id="daily-stability-brief",
                        confirmed_by="ops-admin",
                    )

        self.assertTrue(confirmed_report["confirmed"])
        self.assertEqual(confirmed_report["confirmed_by"], "ops-admin")


if __name__ == "__main__":
    unittest.main()

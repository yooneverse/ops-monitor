import os
import unittest
from unittest.mock import patch

from app.config import reset_settings_cache
from app.services.monitoring_loop import get_monitoring_status, reset_monitoring_state


class MonitoringStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_settings_cache()
        reset_monitoring_state()

    def tearDown(self) -> None:
        reset_settings_cache()
        reset_monitoring_state()

    def test_monitoring_status_includes_runtime_configuration_metadata(self) -> None:
        with patch.dict(
            os.environ,
            {
                "DISCORD_WEBHOOK_URL": "https://discord.example/webhook",
                "MONITOR_USERNAME": "ops-admin",
                "MONITOR_PASSWORD": "s3cret",
                "ENABLE_API_DOCS": "true",
                "MONITOR_INTERVAL_SECONDS": "45",
                "MEMORY_ALERT_THRESHOLD": "75",
                "DISK_ALERT_THRESHOLD": "70",
            },
            clear=False,
        ):
            reset_settings_cache()
            status = get_monitoring_status()

        self.assertTrue(status["enabled"])
        self.assertTrue(status["discord_webhook_configured"])
        self.assertTrue(status["monitor_auth_configured"])
        self.assertTrue(status["api_docs_enabled"])
        self.assertEqual(status["interval_seconds"], 45)
        self.assertEqual(
            status["thresholds"],
            {
                "memory_percent": 75,
                "disk_percent": 70,
            },
        )
        self.assertEqual(status["config_warnings"], [])

    def test_monitoring_status_reports_invalid_runtime_configuration(self) -> None:
        with patch.dict(
            os.environ,
            {
                "MONITOR_INTERVAL_SECONDS": "2",
                "MEMORY_ALERT_THRESHOLD": "high",
                "DISK_ALERT_THRESHOLD": "101",
            },
            clear=False,
        ):
            reset_settings_cache()
            status = get_monitoring_status()

        self.assertEqual(status["interval_seconds"], 30)
        self.assertEqual(
            status["thresholds"],
            {
                "memory_percent": 80,
                "disk_percent": 80,
            },
        )
        self.assertEqual(len(status["config_warnings"]), 3)
        self.assertIn("MONITOR_INTERVAL_SECONDS", status["config_warnings"][0])

    def test_reset_monitoring_state_clears_last_check(self) -> None:
        status = get_monitoring_status()
        self.assertIsNone(status["last_check"])


if __name__ == "__main__":
    unittest.main()

import os
import unittest
from pathlib import Path
from unittest.mock import patch

from app.config import get_settings, reset_settings_cache


class SettingsTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_settings_cache()

    def tearDown(self) -> None:
        reset_settings_cache()

    def test_settings_parse_runtime_configuration(self) -> None:
        with patch.dict(
            os.environ,
            {
                "ALLOWED_HOSTS": "localhost,127.0.0.1,monitor.internal",
                "ENABLE_API_DOCS": "true",
                "ENABLE_MONITORING_LOOP": "false",
                "MONITOR_INTERVAL_SECONDS": "30",
                "MEMORY_ALERT_THRESHOLD": "75",
                "DISK_ALERT_THRESHOLD": "70",
                "LOG_DIR": "custom-logs",
            },
            clear=False,
        ):
            reset_settings_cache()
            settings = get_settings()

        self.assertEqual(
            settings.allowed_hosts,
            ("localhost", "127.0.0.1", "monitor.internal"),
        )
        self.assertTrue(settings.api_docs_enabled)
        self.assertFalse(settings.monitoring_enabled)
        self.assertEqual(settings.monitor_interval_seconds, 30)
        self.assertEqual(settings.memory_alert_threshold, 75)
        self.assertEqual(settings.disk_alert_threshold, 70)
        self.assertEqual(settings.log_dir, Path("custom-logs"))

    def test_reset_settings_cache_reloads_environment_values(self) -> None:
        with patch.dict(os.environ, {"MONITOR_INTERVAL_SECONDS": "60"}, clear=False):
            reset_settings_cache()
            first_settings = get_settings()

        with patch.dict(os.environ, {"MONITOR_INTERVAL_SECONDS": "15"}, clear=False):
            reset_settings_cache()
            second_settings = get_settings()

        self.assertEqual(first_settings.monitor_interval_seconds, 60)
        self.assertEqual(second_settings.monitor_interval_seconds, 15)


if __name__ == "__main__":
    unittest.main()

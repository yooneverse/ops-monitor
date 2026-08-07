import subprocess
import unittest
from unittest.mock import Mock, patch

from app.services.admin_actions import restart_database_service


class AdminActionTests(unittest.TestCase):
    def test_restart_database_service_returns_success(self) -> None:
        completed = Mock(stdout="restarted", stderr="")

        with patch("app.services.admin_actions.subprocess.run", return_value=completed), patch(
            "app.services.admin_actions.add_alert_history"
        ) as add_alert_history:
            result = restart_database_service(requested_by="ops-admin")

        self.assertEqual(result["status"], "ok")
        self.assertIn("restarted", result["message"])
        add_alert_history.assert_called_once()

    def test_restart_database_service_handles_missing_docker(self) -> None:
        with patch("app.services.admin_actions.subprocess.run", side_effect=FileNotFoundError), patch(
            "app.services.admin_actions.add_alert_history"
        ) as add_alert_history:
            result = restart_database_service(requested_by="ops-admin")

        self.assertEqual(result["status"], "error")
        self.assertIn("Docker CLI", result["message"])
        add_alert_history.assert_called_once()

    def test_restart_database_service_handles_command_failure(self) -> None:
        error = subprocess.CalledProcessError(
            returncode=1,
            cmd=["docker", "compose", "restart", "db"],
            stderr="compose failed",
        )

        with patch("app.services.admin_actions.subprocess.run", side_effect=error), patch(
            "app.services.admin_actions.add_alert_history"
        ) as add_alert_history:
            result = restart_database_service(requested_by="ops-admin")

        self.assertEqual(result["status"], "error")
        self.assertIn("compose failed", result["message"])
        add_alert_history.assert_called_once()


if __name__ == "__main__":
    unittest.main()

import subprocess
import unittest
from unittest.mock import Mock, patch

from app.services.admin_actions import restart_database_service


class AdminActionTests(unittest.TestCase):
    def test_restart_database_service_returns_success(self) -> None:
        completed = Mock(stdout="restarted", stderr="")

        with patch("app.services.admin_actions.subprocess.run", return_value=completed):
            result = restart_database_service()

        self.assertEqual(result["status"], "ok")
        self.assertIn("restarted", result["message"])

    def test_restart_database_service_handles_missing_docker(self) -> None:
        with patch("app.services.admin_actions.subprocess.run", side_effect=FileNotFoundError):
            result = restart_database_service()

        self.assertEqual(result["status"], "error")
        self.assertIn("Docker CLI", result["message"])

    def test_restart_database_service_handles_command_failure(self) -> None:
        error = subprocess.CalledProcessError(
            returncode=1,
            cmd=["docker", "compose", "restart", "db"],
            stderr="compose failed",
        )

        with patch("app.services.admin_actions.subprocess.run", side_effect=error):
            result = restart_database_service()

        self.assertEqual(result["status"], "error")
        self.assertIn("compose failed", result["message"])


if __name__ == "__main__":
    unittest.main()

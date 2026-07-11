import os
import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from app.main import build_readiness_response
from app.security import (
    get_allowed_hosts,
    is_docs_enabled,
    require_monitor_auth,
    validate_monitor_credentials,
)
from app.services import db_check
from app.services.monitoring_loop import is_monitoring_enabled


class SecurityConfigTests(unittest.TestCase):
    def test_allowed_hosts_are_split_from_env(self) -> None:
        with patch.dict(os.environ, {"ALLOWED_HOSTS": "localhost,127.0.0.1,monitor.local"}, clear=False):
            self.assertEqual(
                get_allowed_hosts(),
                ["localhost", "127.0.0.1", "monitor.local"],
            )

    def test_docs_flag_defaults_to_disabled(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(is_docs_enabled())

    def test_monitor_credentials_validate_correct_pair(self) -> None:
        with patch.dict(
            os.environ,
            {
                "MONITOR_USERNAME": "ops-admin",
                "MONITOR_PASSWORD": "s3cret",
            },
            clear=False,
        ):
            self.assertTrue(
                validate_monitor_credentials("ops-admin", "s3cret")
            )
            self.assertFalse(
                validate_monitor_credentials("ops-admin", "wrong")
            )

    def test_require_monitor_auth_rejects_missing_configuration(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(HTTPException) as context:
                require_monitor_auth(None)

        self.assertEqual(context.exception.status_code, 503)

    def test_require_monitor_auth_rejects_invalid_credentials(self) -> None:
        with patch.dict(
            os.environ,
            {
                "MONITOR_USERNAME": "ops-admin",
                "MONITOR_PASSWORD": "s3cret",
            },
            clear=False,
        ):
            with self.assertRaises(HTTPException) as context:
                require_monitor_auth(
                    HTTPBasicCredentials(username="ops-admin", password="wrong")
                )

        self.assertEqual(context.exception.status_code, 401)

    def test_require_monitor_auth_accepts_valid_credentials(self) -> None:
        with patch.dict(
            os.environ,
            {
                "MONITOR_USERNAME": "ops-admin",
                "MONITOR_PASSWORD": "s3cret",
            },
            clear=False,
        ):
            username = require_monitor_auth(
                HTTPBasicCredentials(username="ops-admin", password="s3cret")
            )

        self.assertEqual(username, "ops-admin")

    def test_readiness_response_hides_database_details_when_ready(self) -> None:
        payload, status_code = build_readiness_response(
            {
                "status": "connected",
                "message": "Database connection successful",
            }
        )

        self.assertEqual(status_code, 200)
        self.assertEqual(payload["status"], "ready")
        self.assertNotIn("database", payload)

    def test_readiness_response_hides_database_details_when_not_ready(self) -> None:
        payload, status_code = build_readiness_response(
            {
                "status": "disconnected",
                "message": "Database connection failed",
            }
        )

        self.assertEqual(status_code, 503)
        self.assertEqual(payload["status"], "not_ready")
        self.assertNotIn("database", payload)

    def test_monitoring_flag_defaults_to_enabled(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(is_monitoring_enabled())

    def test_monitoring_flag_can_disable_background_loop(self) -> None:
        with patch.dict(os.environ, {"ENABLE_MONITORING_LOOP": "false"}, clear=False):
            self.assertFalse(is_monitoring_enabled())


class DatabaseCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        db_check._engine = None
        db_check._engine_url = None

    def tearDown(self) -> None:
        db_check._engine = None
        db_check._engine_url = None

    def test_database_engine_is_reused_for_same_url(self) -> None:
        fake_engine = MagicMock()

        with patch("app.services.db_check.create_engine", return_value=fake_engine) as create_engine_mock:
            first_engine = db_check.get_database_engine("postgresql://user:pass@db:5432/app")
            second_engine = db_check.get_database_engine("postgresql://user:pass@db:5432/app")

        self.assertIs(first_engine, fake_engine)
        self.assertIs(second_engine, fake_engine)
        create_engine_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()

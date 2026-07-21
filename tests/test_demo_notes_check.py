import unittest
from unittest.mock import Mock, patch

import requests

from app.config import reset_settings_cache
from app.services.demo_notes_check import check_demo_notes_service


class DemoNotesCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_settings_cache()

    def tearDown(self) -> None:
        reset_settings_cache()

    def test_demo_notes_check_returns_disabled_without_url(self) -> None:
        with patch("app.services.demo_notes_check.get_settings") as get_settings_mock:
            get_settings_mock.return_value.demo_notes_url = None

            result = check_demo_notes_service()

        self.assertEqual(result["status"], "disabled")

    def test_demo_notes_check_returns_connected_when_service_is_up(self) -> None:
        response = Mock()
        response.raise_for_status.return_value = None

        with patch("app.services.demo_notes_check.get_settings") as get_settings_mock:
            get_settings_mock.return_value.demo_notes_url = "http://notes:8010/healthz"
            with patch("app.services.demo_notes_check.requests.get", return_value=response):
                result = check_demo_notes_service()

        self.assertEqual(result["status"], "connected")

    def test_demo_notes_check_returns_disconnected_when_request_fails(self) -> None:
        with patch("app.services.demo_notes_check.get_settings") as get_settings_mock:
            get_settings_mock.return_value.demo_notes_url = "http://notes:8010/healthz"
            with patch(
                "app.services.demo_notes_check.requests.get",
                side_effect=requests.RequestException,
            ):
                result = check_demo_notes_service()

        self.assertEqual(result["status"], "disconnected")


if __name__ == "__main__":
    unittest.main()

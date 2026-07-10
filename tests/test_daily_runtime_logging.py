import logging
import os
import unittest
from datetime import datetime
from tempfile import TemporaryDirectory

from app.services.runtime_logs import (
    DailyLogFileHandler,
    get_daily_path,
    persist_alert_event,
)


class DailyRuntimeLoggingTests(unittest.TestCase):
    def test_daily_path_uses_stream_name_and_date(self) -> None:
        with TemporaryDirectory() as temp_dir:
            with unittest.mock.patch.dict(os.environ, {"LOG_DIR": temp_dir}, clear=False):
                path = get_daily_path(
                    stream_name="application",
                    extension="log",
                    now=datetime(2026, 7, 10, 9, 30, 0),
                )

            self.assertEqual(
                str(path).replace("\\", "/"),
                f"{temp_dir.replace(chr(92), '/')}/application/2026-07-10.log",
            )

    def test_persist_alert_event_writes_jsonl_and_markdown_report(self) -> None:
        event = {
            "type": "incident",
            "target": "database",
            "status": "disconnected",
            "message": "Database connection failed",
            "timestamp": "2026-07-10T21:15:00",
        }

        with TemporaryDirectory() as temp_dir:
            with unittest.mock.patch.dict(os.environ, {"LOG_DIR": temp_dir}, clear=False):
                persist_alert_event(event, now=datetime(2026, 7, 10, 21, 15, 0))

                events_path = get_daily_path("events", "jsonl", datetime(2026, 7, 10, 21, 15, 0))
                report_path = get_daily_path("reports", "md", datetime(2026, 7, 10, 21, 15, 0))

                events_text = events_path.read_text(encoding="utf-8")
                report_text = report_path.read_text(encoding="utf-8")

        self.assertIn('"target": "database"', events_text)
        self.assertIn("Ops Monitor Daily Event Report", report_text)
        self.assertIn("Database connection failed", report_text)

    def test_daily_log_handler_writes_to_date_scoped_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            with unittest.mock.patch.dict(os.environ, {"LOG_DIR": temp_dir}, clear=False):
                handler = DailyLogFileHandler(
                    stream_name="application",
                    time_provider=lambda: datetime(2026, 7, 10, 8, 0, 0),
                )
                handler.setFormatter(logging.Formatter("%(message)s"))

                logger = logging.getLogger("tests.daily_runtime_logging")
                original_handlers = list(logger.handlers)
                original_propagate = logger.propagate
                logger.handlers = []
                logger.propagate = False
                logger.setLevel(logging.INFO)
                logger.addHandler(handler)

                try:
                    logger.info("monitoring cycle persisted")
                finally:
                    logger.handlers = original_handlers
                    logger.propagate = original_propagate

                log_path = get_daily_path("application", "log", datetime(2026, 7, 10, 8, 0, 0))
                log_text = log_path.read_text(encoding="utf-8")

        self.assertIn("monitoring cycle persisted", log_text)


if __name__ == "__main__":
    unittest.main()

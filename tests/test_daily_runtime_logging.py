import logging
import os
import unittest
from datetime import datetime
from tempfile import TemporaryDirectory

from app.config import reset_settings_cache
from app.services.runtime_logs import (
    DailyLogFileHandler,
    get_daily_path,
    persist_alert_event,
    persist_monitoring_run,
    read_recent_monitoring_runs,
)


class DailyRuntimeLoggingTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_settings_cache()

    def tearDown(self) -> None:
        reset_settings_cache()

    def test_daily_path_uses_stream_name_and_date(self) -> None:
        with TemporaryDirectory() as temp_dir:
            with unittest.mock.patch.dict(os.environ, {"LOG_DIR": temp_dir}, clear=False):
                reset_settings_cache()
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
                reset_settings_cache()
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
                reset_settings_cache()
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

    def test_persist_monitoring_run_writes_jsonl_and_markdown_report(self) -> None:
        report = {
            "run_id": "20260804-101500",
            "started_at": "2026-08-04T10:15:00",
            "completed_at": "2026-08-04T10:15:02",
            "overall_status": "warning",
            "active_targets": ["database"],
            "excluded_targets": ["demo_notes"],
            "events": [{"type": "incident"}],
        }

        with TemporaryDirectory() as temp_dir:
            with unittest.mock.patch.dict(os.environ, {"LOG_DIR": temp_dir}, clear=False):
                reset_settings_cache()
                persist_monitoring_run(report, now=datetime(2026, 8, 4, 10, 15, 2))

                runs_path = get_daily_path("runs", "jsonl", datetime(2026, 8, 4, 10, 15, 2))
                markdown_path = get_daily_path("run-reports", "md", datetime(2026, 8, 4, 10, 15, 2))

                runs_text = runs_path.read_text(encoding="utf-8")
                markdown_text = markdown_path.read_text(encoding="utf-8")

        self.assertIn('"run_id": "20260804-101500"', runs_text)
        self.assertIn("Ops Monitor Monitoring Run Report", markdown_text)
        self.assertIn("demo_notes", markdown_text)

    def test_read_recent_monitoring_runs_returns_latest_entries_first(self) -> None:
        earlier_report = {
            "run_id": "20260803-221500",
            "completed_at": "2026-08-03T22:15:02",
            "overall_status": "ok",
            "active_targets": ["database"],
            "excluded_targets": [],
            "events": [],
        }
        latest_report = {
            "run_id": "20260804-101500",
            "completed_at": "2026-08-04T10:15:02",
            "overall_status": "warning",
            "active_targets": ["database"],
            "excluded_targets": ["demo_notes"],
            "events": [{"type": "incident"}],
        }

        with TemporaryDirectory() as temp_dir:
            with unittest.mock.patch.dict(os.environ, {"LOG_DIR": temp_dir}, clear=False):
                reset_settings_cache()
                persist_monitoring_run(earlier_report, now=datetime(2026, 8, 3, 22, 15, 2))
                persist_monitoring_run(latest_report, now=datetime(2026, 8, 4, 10, 15, 2))

                recent_reports = read_recent_monitoring_runs(limit=2)

        self.assertEqual([report["run_id"] for report in recent_reports], ["20260804-101500", "20260803-221500"])


if __name__ == "__main__":
    unittest.main()

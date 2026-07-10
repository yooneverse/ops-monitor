import json
import logging
import os
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Callable

from dotenv import load_dotenv

_write_lock = Lock()


def load_runtime_env() -> None:
    load_dotenv(override=True)


def get_log_dir() -> Path:
    load_runtime_env()
    return Path(os.getenv("LOG_DIR", "logs"))


def get_daily_path(
    stream_name: str,
    extension: str,
    now: datetime | None = None,
) -> Path:
    target_time = now or datetime.now()
    return get_log_dir() / stream_name / f"{target_time:%Y-%m-%d}.{extension}"


def append_text_line(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with _write_lock:
        with path.open("a", encoding="utf-8") as file:
            file.write(f"{line}\n")


def sanitize_report_value(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ").strip()


def build_report_header(report_date: str) -> str:
    return "\n".join(
        [
            "# Ops Monitor Daily Event Report",
            "",
            f"Date: {report_date}",
            "",
            "| Time | Type | Target | Status | Message |",
            "|---|---|---|---|---|",
        ]
    )


def persist_alert_event(event: dict, now: datetime | None = None) -> None:
    target_time = now or datetime.now()

    jsonl_path = get_daily_path("events", "jsonl", target_time)
    append_text_line(jsonl_path, json.dumps(event, ensure_ascii=False))

    report_path = get_daily_path("reports", "md", target_time)
    report_date = target_time.strftime("%Y-%m-%d")

    if not report_path.exists():
        append_text_line(report_path, build_report_header(report_date))

    report_row = (
        f"| {sanitize_report_value(event.get('timestamp', ''))} "
        f"| {sanitize_report_value(event.get('type', ''))} "
        f"| {sanitize_report_value(event.get('target', ''))} "
        f"| {sanitize_report_value(event.get('status', ''))} "
        f"| {sanitize_report_value(event.get('message', ''))} |"
    )
    append_text_line(report_path, report_row)


class DailyLogFileHandler(logging.Handler):
    def __init__(
        self,
        stream_name: str,
        time_provider: Callable[[], datetime] | None = None,
    ) -> None:
        super().__init__()
        self.stream_name = stream_name
        self.time_provider = time_provider or datetime.now

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record)
            log_path = get_daily_path(self.stream_name, "log", self.time_provider())
            append_text_line(log_path, message)
        except Exception:
            self.handleError(record)


def attach_daily_handler(logger_name: str, stream_name: str) -> None:
    logger = logging.getLogger(logger_name)

    for handler in logger.handlers:
        if isinstance(handler, DailyLogFileHandler) and handler.stream_name == stream_name:
            return

    handler = DailyLogFileHandler(stream_name=stream_name)
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    logger.addHandler(handler)


def configure_runtime_logging() -> None:
    attach_daily_handler("uvicorn.error", "application")
    attach_daily_handler("uvicorn.access", "access")

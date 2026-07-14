import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

TRUE_VALUES = {"1", "true", "yes", "on"}


def parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default

    return value.strip().lower() in TRUE_VALUES


def parse_csv(value: str | None, default: tuple[str, ...]) -> tuple[str, ...]:
    if value is None:
        return default

    values = tuple(item.strip() for item in value.split(",") if item.strip())
    return values or default


@dataclass(frozen=True)
class Settings:
    database_url: str | None
    discord_webhook_url: str | None
    monitor_username: str | None
    monitor_password: str | None
    allowed_hosts: tuple[str, ...]
    api_docs_enabled: bool
    monitoring_enabled: bool
    monitor_interval_seconds: int
    memory_alert_threshold: int
    disk_alert_threshold: int
    log_dir: Path

    @property
    def monitor_auth_configured(self) -> bool:
        return bool(self.monitor_username and self.monitor_password)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv(override=False)

    return Settings(
        database_url=os.getenv("DATABASE_URL"),
        discord_webhook_url=os.getenv("DISCORD_WEBHOOK_URL"),
        monitor_username=os.getenv("MONITOR_USERNAME"),
        monitor_password=os.getenv("MONITOR_PASSWORD"),
        allowed_hosts=parse_csv(
            os.getenv("ALLOWED_HOSTS"),
            default=("localhost", "127.0.0.1", "testserver"),
        ),
        api_docs_enabled=parse_bool(os.getenv("ENABLE_API_DOCS"), default=False),
        monitoring_enabled=parse_bool(os.getenv("ENABLE_MONITORING_LOOP"), default=True),
        monitor_interval_seconds=int(os.getenv("MONITOR_INTERVAL_SECONDS", "30")),
        memory_alert_threshold=int(os.getenv("MEMORY_ALERT_THRESHOLD", "80")),
        disk_alert_threshold=int(os.getenv("DISK_ALERT_THRESHOLD", "80")),
        log_dir=Path(os.getenv("LOG_DIR", "logs")),
    )


def reset_settings_cache() -> None:
    get_settings.cache_clear()

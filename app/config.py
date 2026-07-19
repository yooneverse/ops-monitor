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


def normalize_optional_str(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def read_int_setting(
    env_name: str,
    default: int,
    warnings: list[str],
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    raw_value = os.getenv(env_name)

    if raw_value is None:
        return default

    try:
        parsed_value = int(raw_value.strip())
    except ValueError:
        warnings.append(
            f"{env_name} must be an integer. Using default value {default}."
        )
        return default

    if minimum is not None and parsed_value < minimum:
        warnings.append(
            f"{env_name} must be greater than or equal to {minimum}. Using default value {default}."
        )
        return default

    if maximum is not None and parsed_value > maximum:
        warnings.append(
            f"{env_name} must be less than or equal to {maximum}. Using default value {default}."
        )
        return default

    return parsed_value


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
    config_warnings: tuple[str, ...]

    @property
    def monitor_auth_configured(self) -> bool:
        return bool(self.monitor_username and self.monitor_password)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv(override=False)
    config_warnings: list[str] = []

    return Settings(
        database_url=normalize_optional_str(os.getenv("DATABASE_URL")),
        discord_webhook_url=normalize_optional_str(os.getenv("DISCORD_WEBHOOK_URL")),
        monitor_username=normalize_optional_str(os.getenv("MONITOR_USERNAME")),
        monitor_password=normalize_optional_str(os.getenv("MONITOR_PASSWORD")),
        allowed_hosts=parse_csv(
            os.getenv("ALLOWED_HOSTS"),
            default=("localhost", "127.0.0.1", "testserver"),
        ),
        api_docs_enabled=parse_bool(os.getenv("ENABLE_API_DOCS"), default=False),
        monitoring_enabled=parse_bool(os.getenv("ENABLE_MONITORING_LOOP"), default=True),
        monitor_interval_seconds=read_int_setting(
            "MONITOR_INTERVAL_SECONDS",
            30,
            config_warnings,
            minimum=5,
            maximum=3600,
        ),
        memory_alert_threshold=read_int_setting(
            "MEMORY_ALERT_THRESHOLD",
            80,
            config_warnings,
            minimum=1,
            maximum=100,
        ),
        disk_alert_threshold=read_int_setting(
            "DISK_ALERT_THRESHOLD",
            80,
            config_warnings,
            minimum=1,
            maximum=100,
        ),
        log_dir=Path(normalize_optional_str(os.getenv("LOG_DIR")) or "logs"),
        config_warnings=tuple(config_warnings),
    )


def reset_settings_cache() -> None:
    get_settings.cache_clear()

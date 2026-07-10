import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

basic_auth = HTTPBasic(auto_error=False)


def load_runtime_env() -> None:
    load_dotenv(override=True)


def parse_bool_env(name: str, default: bool = False) -> bool:
    load_runtime_env()
    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def get_allowed_hosts() -> list[str]:
    load_runtime_env()
    raw_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")

    hosts = [host.strip() for host in raw_hosts.split(",") if host.strip()]

    if not hosts:
        return ["localhost", "127.0.0.1", "testserver"]

    return hosts


def is_docs_enabled() -> bool:
    return parse_bool_env("ENABLE_API_DOCS", default=False)


def get_monitor_credentials() -> tuple[str | None, str | None]:
    load_runtime_env()
    return (
        os.getenv("MONITOR_USERNAME"),
        os.getenv("MONITOR_PASSWORD"),
    )


def is_monitor_auth_configured() -> bool:
    username, password = get_monitor_credentials()
    return bool(username and password)


def validate_monitor_credentials(
    username: str | None,
    password: str | None,
) -> bool:
    expected_username, expected_password = get_monitor_credentials()

    if not expected_username or not expected_password:
        return False

    if username is None or password is None:
        return False

    username_matches = secrets.compare_digest(username, expected_username)
    password_matches = secrets.compare_digest(password, expected_password)

    return username_matches and password_matches


def require_monitor_auth(
    credentials: HTTPBasicCredentials | None = Depends(basic_auth),
) -> str:
    if not is_monitor_auth_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Monitoring authentication is not configured",
        )

    if not credentials or not validate_monitor_credentials(
        credentials.username,
        credentials.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username

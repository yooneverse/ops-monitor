import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import get_settings

basic_auth = HTTPBasic(auto_error=False)


def get_allowed_hosts() -> list[str]:
    return list(get_settings().allowed_hosts)


def is_docs_enabled() -> bool:
    return get_settings().api_docs_enabled


def get_monitor_credentials() -> tuple[str | None, str | None]:
    settings = get_settings()
    return (
        settings.monitor_username,
        settings.monitor_password,
    )


def is_monitor_auth_configured() -> bool:
    return get_settings().monitor_auth_configured


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

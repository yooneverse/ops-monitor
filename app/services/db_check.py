import logging
from pathlib import Path

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings

logger = logging.getLogger("uvicorn.error")

_engine: Engine | None = None
_engine_url: str | None = None


def is_running_in_container() -> bool:
    return Path("/.dockerenv").exists()


def normalize_database_url(database_url: str) -> str:
    if is_running_in_container():
        return database_url

    try:
        parsed = make_url(database_url)
    except Exception:
        return database_url

    if parsed.host != "db":
        return database_url

    return str(parsed.set(host="localhost"))


def get_database_url() -> str | None:
    database_url = get_settings().database_url

    if not database_url:
        return None

    return normalize_database_url(database_url)


def reset_database_engine_cache() -> None:
    global _engine
    global _engine_url

    if _engine is not None:
        _engine.dispose()

    _engine = None
    _engine_url = None


def get_database_engine(database_url: str) -> Engine:
    global _engine
    global _engine_url

    if _engine is not None and _engine_url == database_url:
        return _engine

    connect_args: dict[str, int] = {}

    if database_url.startswith("postgresql"):
        connect_args["connect_timeout"] = 3

    _engine = create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
    _engine_url = database_url
    return _engine


def check_database_connection():
    database_url = get_database_url()

    logger.info("Checking database connection...")

    if not database_url:
        logger.error("DATABASE_URL is not set")
        return {
            "status": "error",
            "message": "DATABASE_URL is not set",
        }

    try:
        engine = get_database_engine(database_url)

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "message": "Database connection successful",
        }

    except SQLAlchemyError:
        logger.exception("Database connection failed")
        return {
            "status": "disconnected",
            "message": "Database connection failed",
        }

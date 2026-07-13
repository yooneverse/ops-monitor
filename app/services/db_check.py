import logging

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings

logger = logging.getLogger("uvicorn.error")

_engine: Engine | None = None
_engine_url: str | None = None


def get_database_url() -> str | None:
    return get_settings().database_url


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

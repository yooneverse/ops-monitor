import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("uvicorn.error")


def check_database_connection():
    load_dotenv(override=True)
    database_url = os.getenv("DATABASE_URL")

    logger.info("Checking database connection...")

    if not database_url:
        logger.error("DATABASE_URL is not set")
        return {
            "status": "error",
            "message": "DATABASE_URL is not set",
        }

    try:
        engine = create_engine(database_url)

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

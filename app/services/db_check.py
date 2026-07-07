import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def check_database_connection():
    load_dotenv(override=True)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
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
        return {
            "status": "disconnected",
            "message": "Database connection failed",
        }

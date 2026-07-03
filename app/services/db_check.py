import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def check_database_connection():
    if not DATABASE_URL:
        return {
            "status": "error",
            "message": "DATABASE_URL is not set"
        }

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "message": "Database connection successful"
        }

    except Exception as error:
        return {
            "status": "disconnected",
            "message": str(error)
        }
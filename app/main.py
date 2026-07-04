from datetime import datetime

from fastapi import FastAPI

from app.services.db_check import check_database_connection

app = FastAPI(title="Ops Monitor")


@app.get("/")
def root():
    return {
        "message": "Ops Monitor API is running"
    }


@app.get("/health")
def health_check():
    database_status = check_database_connection()

    return {
        "api": "ok",
        "database": database_status,
        "timestamp": datetime.now().isoformat()
    }
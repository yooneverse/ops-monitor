from fastapi import FastAPI
from datetime import datetime

from app.services.db_check import check_database_connection

app = FastAPI(title="Ops Monitor")


@app.get("/")
def root():
    return {
        "message": "Ops Monitor API is running"
    }


@app.get("/health")
def health_check():
    db_status = check_database_connection()

    return {
        "api": "ok",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    }
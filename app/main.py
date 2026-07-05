from datetime import datetime

from app.api.dashboard import router as dashboard_router

from fastapi import FastAPI

from app.services.db_check import check_database_connection

from app.services.system_check import check_system_status

app = FastAPI(title="Ops Monitor")

app.include_router(dashboard_router)


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
    
@app.get("/system")
def system_status():
    return check_system_status()
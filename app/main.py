from datetime import datetime

from app.api.dashboard import router as dashboard_router

from fastapi import FastAPI

from app.services.db_check import check_database_connection

from app.services.system_check import check_system_status

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ops Monitor")

app.include_router(dashboard_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

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
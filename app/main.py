from datetime import datetime

from app.api.dashboard import router as dashboard_router
from app.services.monitoring_loop import monitor_services

from fastapi import FastAPI

from app.services.db_check import check_database_connection
from app.services.system_check import check_system_status

from fastapi.middleware.cors import CORSMiddleware

import asyncio

app = FastAPI(title="Ops Monitor")

app.include_router(dashboard_router)

monitoring_task = None

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

@app.on_event("startup")
async def startup_event():
    global monitoring_task
    monitoring_task = asyncio.create_task(monitor_services())


@app.on_event("shutdown")
async def shutdown_event():
    global monitoring_task

    if monitoring_task:
        monitoring_task.cancel()

        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass
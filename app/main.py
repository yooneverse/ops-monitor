from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Ops Monitor")

@app.get("/")
def root():
    return {
        "message": "Ops Monitor API is running"
    }

@app.get("/health")
def health_check():
    return {
        "api": "ok",
        "timestamp": datetime.now().isoformat()
    }
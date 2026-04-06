from fastapi import FastAPI
import os
from datetime import datetime

app = FastAPI(title="LaunchPad", description="Auto-deployed via Docker + GitHub Actions + AWS EC2")

@app.get("/")
def root():
    return{
        "message": "Hello from LaunchPad!",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health():
    return{"status": "high sir"}
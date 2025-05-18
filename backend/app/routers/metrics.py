from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import PredictionLog
from datetime import datetime, timedelta

router = APIRouter(prefix="/metrics", tags=["metrics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/24h")
def accuracy_last_24h(db: Session = Depends(get_db)):
    cutoff = datetime.now() - timedelta(hours=24)
    logs = db.query(PredictionLog).filter(PredictionLog.timestamp >= cutoff).all()

    if not logs:
        return {"errors": []}

    return {
        "errors": [
            log.error for log in logs
        ],
    }

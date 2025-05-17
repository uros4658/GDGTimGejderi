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
    cutoff = datetime.utcnow() - timedelta(hours=24)
    logs = db.query(PredictionLog).filter(PredictionLog.timestamp >= cutoff).all()

    if not logs:
        return {"accuracy": None, "total": 0}

    correct = sum(1 for log in logs if (log.will_change and log.confidence >= 0.5) or
                                           (not log.will_change and log.confidence < 0.5))
    return {
        "accuracy": round(correct / len(logs), 4),
        "total": len(logs)
    }

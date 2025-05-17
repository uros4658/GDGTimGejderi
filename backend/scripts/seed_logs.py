from app.models import PredictionLog, VesselCall
from app.db import SessionLocal
from datetime import datetime, timedelta
import random

session = SessionLocal()

# Get all valid vessel_call IDs
vessel_call_ids = [row.id for row in session.query(VesselCall.id).all()]
if not vessel_call_ids:
    print("No vessel_calls found! Seed vessel_calls first.")
else:
    for i in range(20):
        session.add(PredictionLog(
            vessel_call_id=random.choice(vessel_call_ids),
            timestamp=datetime.utcnow() - timedelta(minutes=i * 30),
            will_change=random.choice([True, False]),
            confidence=round(random.uniform(0.3, 0.9), 2),
            model_version="v0.1.0"
        ))
    session.commit()
session.close()
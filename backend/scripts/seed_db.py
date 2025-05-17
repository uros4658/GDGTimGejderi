import random
from datetime import datetime, timedelta
from app.db import SessionLocal
from app.models import VesselCall, Berth

def seed_berths(session):
    names = ["A1", "B2", "C3", "D4"]
    for name in names:
        session.add(Berth(
            name=name,
            length_m=random.uniform(150, 300),
            depth_m=random.uniform(8, 16)
        ))

def seed_vessels(session):
    now = datetime.utcnow()
    for i in range(25):
        eta = now + timedelta(hours=random.randint(1, 48))
        etd = eta + timedelta(hours=random.randint(4, 12))
        berth = random.choice(["A1", "B2", "C3", "D4"])
        session.add(VesselCall(
            imo=9000000 + i,
            eta=eta,
            etd=etd,
            planned_berth=berth,
            predicted_change=random.choice([True, False]),
            prediction_confidence=round(random.uniform(0.5, 0.99), 2),
        ))

if __name__ == "__main__":
    session = SessionLocal()
    seed_berths(session)
    seed_vessels(session)
    session.commit()
    session.close()
    print("✅ Seeded vessels + berths.")

import random
from datetime import datetime, timedelta
from app.db import SessionLocal
from app.models import VesselCall, Berth
from app.models import VesselCall, Berth, Weather  # import Weather
from sqlalchemy import func


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

    # Get list of all berths
    berth_names = [berth.name for berth in session.query(Berth).all()]

    for i in range(25):
        eta = now + timedelta(hours=random.randint(1, 48))
        etd = eta + timedelta(hours=random.randint(4, 12))
        berth = random.choice(berth_names)

        # Get the closest weather record to ETA (within 2 hours range)
        weather = session.query(Weather)\
            .order_by(func.abs(func.extract("epoch", Weather.timestamp - eta)))\
            .first()

        vc = VesselCall(
            imo=9000000 + i,
            vessel_name=f"Vessel-{i}",
            vessel_type=random.choice(["CONTAINER", "BULK", "RORO", "TANKER"]),
            loa_m=random.uniform(180, 300),
            beam_m=random.uniform(20, 40),
            draft_m=random.uniform(8, 14),
            eta=eta,
            etd=etd,
            optimizer_berth_id=berth,
            optimizer_start=eta - timedelta(hours=1),
            optimizer_end=etd,
            predicted_change=random.choice([True, False]),
            prediction_confidence=round(random.uniform(0.5, 0.99), 2),
            weather_id=weather.id if weather else None  # fallback if no weather exists yet
        )
        session.add(vc)
    now = datetime.utcnow()
    
        
        

if __name__ == "__main__":
    session = SessionLocal()
    seed_berths(session)
    seed_vessels(session)
    session.commit()
    session.close()
    print("✅ Seeded vessels + berths.")

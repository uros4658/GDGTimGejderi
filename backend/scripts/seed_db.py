import random
from datetime import datetime, timedelta
from app.db import SessionLocal
from app.models import VesselCall, Berth, Weather, MaintenanceLog
from sqlalchemy import func



def seed_weather(session):
    print("⛅ Seeding weather...")
    base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0) - timedelta(hours=12)
    conditions = ["CLEAR", "RAIN", "STORM"]
    weights = [0.7, 0.2, 0.1]  # Summer bias

    for hour in range(96):  # ~4 days hourly
        ts = base_time + timedelta(hours=hour)
        condition = random.choices(conditions, weights)[0]
        session.add(Weather(
            timestamp=ts,
            condition=condition,
            temperature_c=random.uniform(24, 35),
            wind_speed_knots=random.uniform(2, 18),
            tide_height_m=random.uniform(0.8, 1.8)
        ))

def seed_maintenance_logs(session):
    print("🔧 Seeding maintenance logs...")
    now = datetime.utcnow()
    for berth in session.query(Berth).all():
        # Simulate 1–3 past events per berth
        for i in range(random.randint(1, 3)):
            performed_at = now - timedelta(days=random.randint(5, 60))
            session.add(MaintenanceLog(
                berth_name=berth.name,
                performed_at=performed_at,
                notes=random.choice(["Routine", "Crane repair", "Surface cleaning"])
            ))
def seed_berths(session):
    maint_ids = [m.id for m in session.query(MaintenanceLog.id).all()]
    names = ["A1", "B2", "C3", "D4"]
    berth_specs = [
        {"max_loa": 350, "max_beam": 50, "max_draft": 15, "max_dwt": 120000, "allowed_types": "CONTAINER,BULK"},
        {"max_loa": 250, "max_beam": 38, "max_draft": 13, "max_dwt": 80000, "allowed_types": "BULK,RORO"},
        {"max_loa": 220, "max_beam": 35, "max_draft": 11, "max_dwt": 60000, "allowed_types": "RORO,TANKER"},
        {"max_loa": 400, "max_beam": 60, "max_draft": 16, "max_dwt": 150000, "allowed_types": "CONTAINER,TANKER"},
    ]
    for name, spec in zip(names, berth_specs):
        maintenance_id = random.choice(maint_ids) if maint_ids and random.random() < 0.5 else None
        session.add(Berth(
            name=name,
            length_m=spec["max_loa"],
            depth_m=spec["max_draft"],
            max_loa=spec["max_loa"],
            max_beam=spec["max_beam"],
            max_draft=spec["max_draft"],
            max_dwt=spec["max_dwt"],
            allowed_types=spec["allowed_types"],
            maintenance_id=maintenance_id
        ))
        
def seed_vessels(session):
    print("🚢 Seeding vessels with ATA and ABA...")
    now = datetime.utcnow()
    berth_names = [b.name for b in session.query(Berth).all()]

    for i in range(25):
        eta = now + timedelta(hours=random.randint(1, 48))
        etd = eta + timedelta(hours=random.randint(4, 12))
        berth = random.choice(berth_names)
       

        # Find closest weather to ETA
        weather = session.query(Weather)\
            .order_by(func.abs(func.extract("epoch", Weather.timestamp - eta)))\
            .first()

        weather_delay_min = 0
        if weather:
            if weather.condition == "CLEAR":
                weather_delay_min = 0
            elif weather.condition == "RAIN":
                weather_delay_min = random.randint(10, 30)
            elif weather.condition == "STORM":
                weather_delay_min = random.randint(30, 90)

        # Find last maintenance at the berth
        recent_maint = session.query(MaintenanceLog)\
            .filter(MaintenanceLog.berth_name == berth)\
            .order_by(MaintenanceLog.performed_at.desc())\
            .first()

        maint_penalty = 0
        if recent_maint:
            days_since = (eta - recent_maint.performed_at).days
            if days_since <= 10:
                maint_penalty = -10  # recently maintained = less delay
            elif days_since >= 30:
                maint_penalty = +10  # old maintenance = slight delay

        # Compute delay (net effect)
        net_delay_min = max(0, weather_delay_min + maint_penalty)
        ata = eta + timedelta(minutes=net_delay_min)
        aba = ata + timedelta(minutes=random.randint(0, 20))  # loading window slack

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
            weather_id=weather.id if weather else None,
            ata=ata,
            aba=aba        )
        session.add(vc)


# Run all
if __name__ == "__main__":
    session = SessionLocal()
    seed_berths(session)
    session.commit()  # required before referencing berths

    seed_weather(session)
    session.commit()

    seed_maintenance_logs(session)
    session.commit()

    seed_vessels(session)
    session.commit()

    session.close()
    print("✅ All data seeded.")

import random
from datetime import datetime, timedelta
from app.db import SessionLocal
from app.models import Weather, Berth, MaintenanceLog, Vessel, PredictionScheduleEntry

def seed_weather(session, n=96):
    print("⛅ Seeding weather...")
    base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0) - timedelta(hours=12)
    conditions = ["CLEAR", "RAIN", "STORM"]
    weights = [0.7, 0.2, 0.1]
    for i in range(n):
        ts = base_time + timedelta(hours=i)
        cond = random.choices(conditions, weights)[0]
        session.add(Weather(
            timestamp=ts,
            condition=cond,
            temperature_c=random.uniform(24, 35),
            wind_speed_knots=random.uniform(2, 18),
            tide_height_m=random.uniform(0.8, 1.8)
        ))

def seed_berths(session):
    print("🛳️ Seeding berths...")
    names = ["A1", "B2", "C3", "D4"]
    specs = [
        {"max_loa": 350, "max_beam": 50, "max_draft": 15, "max_dwt": 120000, "allowed_types": "CONTAINER,BULK"},
        {"max_loa": 250, "max_beam": 38, "max_draft": 13, "max_dwt": 80000, "allowed_types": "BULK,RORO"},
        {"max_loa": 220, "max_beam": 35, "max_draft": 11, "max_dwt": 60000, "allowed_types": "RORO,TANKER"},
        {"max_loa": 400, "max_beam": 60, "max_draft": 16, "max_dwt": 150000, "allowed_types": "CONTAINER,TANKER"},
    ]
    for name, spec in zip(names, specs):
        session.add(Berth(
            name=name,
            depth_m=spec["max_draft"],
            max_loa=spec["max_loa"],
            max_beam=spec["max_beam"],
            max_draft=spec["max_draft"],
            max_dwt=spec["max_dwt"],
            allowed_types=spec["allowed_types"],
            maintenance_id=None
        ))

def seed_maintenance_logs(session):
    print("🔧 Seeding maintenance logs...")
    now = datetime.utcnow()
    logs = []
    for berth in session.query(Berth).all():
        for _ in range(random.randint(1, 3)):
            performed_at = now - timedelta(days=random.randint(5, 60))
            log = MaintenanceLog(
                berth_name=berth.name,
                performed_at=performed_at,
                notes=random.choice(["Routine", "Crane repair", "Surface cleaning"])
            )
            session.add(log)
            logs.append(log)
    session.flush()  # So logs get IDs
    # Assign latest maintenance log to each berth
    for berth in session.query(Berth).all():
        logs_for_berth = [log for log in logs if log.berth_name == berth.name]
        if logs_for_berth:
            latest_log = max(logs_for_berth, key=lambda l: l.performed_at)
            berth.maintenance_id = latest_log.id

def seed_vessels(session, n=25):
    print("🚢 Seeding vessels...")
    now = datetime.utcnow()
    berths = session.query(Berth).all()
    for i in range(n):
        eta = now + timedelta(hours=random.randint(1, 48))
        vessel = Vessel(
            actual_id=1000,
            name=f"Vessel-{i}",
            type=random.choice(["CONTAINER", "BULK", "RORO", "TANKER"]),
            loa_m=random.uniform(180, 300),
            beam_m=random.uniform(20, 40),
            draft_m=random.uniform(8, 14),
            dwt_t=random.uniform(20000, 120000),
            eta=eta,
            ebt=random.uniform(1, 10)
        )
        session.add(vessel)
    session.flush()  # So vessels get IDs

def seed_schedule_entries(session):
    print("📅 Seeding schedule entries...")
    vessels = session.query(Vessel).all()
    berths = session.query(Berth).all()
    for i, vessel in enumerate(vessels):
        berth = random.choice(berths)
        start_time = vessel.eta + timedelta(minutes=random.randint(0, 60))
        end_time = start_time + timedelta(hours=random.randint(4, 12))
        session.add(PredictionScheduleEntry(
            schedule_id=1,
            berth_id=berth.id,
            vessel_id=vessel.id,
            start_time=start_time,
            end_time=end_time
        ))

if __name__ == "__main__":
    session = SessionLocal()
    seed_berths(session)
    session.commit()

    seed_weather(session)
    session.commit()

    seed_maintenance_logs(session)
    session.commit()

    seed_vessels(session)
    session.commit()

    seed_schedule_entries(session)
    session.commit()

    session.close()
    print("✅ All tables seeded with realistic data.")
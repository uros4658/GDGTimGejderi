import random
from datetime import datetime, timedelta
from app.db import SessionLocal
from app.models import Weather, Berth, MaintenanceLog, Vessel, PredictionScheduleEntry

VESSEL_TYPES = ["CONTAINER", "BULK", "RORO", "TANKER"]
BERTH_NAMES = ["A2", "B3", "C4", "D5"]
BERTH_SPECS = [
    {"max_loa": 350, "max_beam": 50, "max_draft": 15, "max_dwt": 120000, "allowed_types": "CONTAINER,BULK"},
    {"max_loa": 250, "max_beam": 38, "max_draft": 13, "max_dwt": 80000, "allowed_types": "BULK,RORO"},
    {"max_loa": 220, "max_beam": 35, "max_draft": 11, "max_dwt": 60000, "allowed_types": "RORO,TANKER"},
    {"max_loa": 400, "max_beam": 60, "max_draft": 16, "max_dwt": 150000, "allowed_types": "CONTAINER,TANKER"},
]
    
def seed_weather(session, n=120):
    print("⛅ Seeding weather...")
    base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0) - timedelta(hours=24)
    conditions = ["CLEAR", "RAIN", "STORM"]
    weights = [0.7, 0.2, 0.1]
    for i in range(n):
        ts = base_time + timedelta(hours=i)
        cond = random.choices(conditions, weights)[0]
        session.add(Weather(
            timestamp=ts,
            condition=cond,
            temperature_c=round(random.uniform(18, 36), 1),
            wind_speed_knots=round(random.uniform(1, 22), 1),
            tide_height_m=round(random.uniform(0.5, 2.2), 2)
        ))

def seed_berths(session):
    print("🛳️ Seeding berths...")
    for name, spec in zip(BERTH_NAMES, BERTH_SPECS):
        session.add(Berth(
            name=name,
            depth_m=spec["max_draft"] + round(random.uniform(0, 2), 1),
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
        for _ in range(random.randint(2, 4)):
            performed_at = now - timedelta(days=random.randint(3, 90))
            log = MaintenanceLog(
                berth_name=berth.name,
                performed_at=performed_at,
                notes=random.choice(["Routine", "Crane repair", "Surface cleaning", "Dock inspection"])
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

def seed_vessels(session, n=60):
    print("🚢 Seeding vessels...")
    now = datetime.utcnow()
    vessels = []
    for i in range(n):
        vessel_type = random.choice(VESSEL_TYPES)
        # Pick a berth that allows this vessel type
        allowed_berths = [b for b, spec in zip(BERTH_NAMES, BERTH_SPECS) if vessel_type in spec["allowed_types"].split(",")]
        berth_name = random.choice(allowed_berths)
        berth_spec = BERTH_SPECS[BERTH_NAMES.index(berth_name)]
        loa = round(random.uniform(berth_spec["max_loa"] * 0.7, berth_spec["max_loa"]), 1)
        beam = round(random.uniform(berth_spec["max_beam"] * 0.7, berth_spec["max_beam"]), 1)
        draft = round(random.uniform(berth_spec["max_draft"] * 0.7, berth_spec["max_draft"]), 1)
        dwt = round(random.uniform(berth_spec["max_dwt"] * 0.5, berth_spec["max_dwt"]), 1)
        eta = now + timedelta(hours=random.randint(1, 120))
        ebt = random.randint(60, 360)  # minutes
        vessel = Vessel(
            actual_id=1000,
            name=f"{vessel_type.capitalize()} Vessel {i+1}",
            type=vessel_type,
            loa_m=loa,
            beam_m=beam,
            draft_m=draft,
            dwt_t=dwt,
            eta=eta,
            ebt=ebt
        )
        session.add(vessel)
        vessels.append((vessel, berth_name))
    session.flush()  # So vessels get IDs
    return vessels

def seed_schedule_entries(session, vessel_berth_pairs):
    print("📅 Seeding schedule entries...")
    for vessel, berth_name in vessel_berth_pairs:
        berth = session.query(Berth).filter_by(name=berth_name).first()
        start_time = vessel.eta + timedelta(minutes=random.randint(0, 60))
        end_time = start_time + timedelta(minutes=vessel.ebt)
        session.add(PredictionScheduleEntry(
            schedule_id=1,
            actual_id=vessel.actual_id,
            berth_id=berth.id,
            vessel_id=vessel.id,
            start_time=start_time,
            end_time=end_time,
            actual_start_time=None,
            actual_end_time=None
        ))

if __name__ == "__main__":
    session = SessionLocal()
    seed_berths(session)
    session.commit()

    seed_weather(session)
    session.commit()

    seed_maintenance_logs(session)
    session.commit()

    vessel_berth_pairs = seed_vessels(session, n=120)
    session.commit()

    seed_schedule_entries(session, vessel_berth_pairs)
    session.commit()

    session.close()
    print("✅ All tables seeded with realistic and consistent data.")
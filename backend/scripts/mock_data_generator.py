import random
import json
from datetime import datetime, timedelta

def random_dt(start, end):
    """Return a random datetime between start and end."""
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate_weather(n=96):
    base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0) - timedelta(hours=12)
    conditions = ["CLEAR", "RAIN", "STORM"]
    weights = [0.7, 0.2, 0.1]
    weather = []
    for i in range(n):
        ts = base_time + timedelta(hours=i)
        cond = random.choices(conditions, weights)[0]
        weather.append({
            "id": i+1,
            "timestamp": ts.isoformat(),
            "condition": cond,
            "temperature_c": round(random.uniform(24, 35), 1),
            "wind_speed_knots": round(random.uniform(2, 18), 1),
            "tide_height_m": round(random.uniform(0.8, 1.8), 2)
        })
    return weather

def generate_berths():
    names = ["A1", "B2", "C3", "D4"]
    specs = [
        {"max_loa": 350, "max_beam": 50, "max_draft": 15, "max_dwt": 120000, "allowed_types": "CONTAINER,BULK"},
        {"max_loa": 250, "max_beam": 38, "max_draft": 13, "max_dwt": 80000, "allowed_types": "BULK,RORO"},
        {"max_loa": 220, "max_beam": 35, "max_draft": 11, "max_dwt": 60000, "allowed_types": "RORO,TANKER"},
        {"max_loa": 400, "max_beam": 60, "max_draft": 16, "max_dwt": 150000, "allowed_types": "CONTAINER,TANKER"},
    ]
    berths = []
    for i, (name, spec) in enumerate(zip(names, specs)):
        berths.append({
            "id": i+1,
            "name": name,
            "depth_m": spec["max_draft"],
            "max_loa": spec["max_loa"],
            "max_beam": spec["max_beam"],
            "max_draft": spec["max_draft"],
            "max_dwt": spec["max_dwt"],
            "allowed_types": spec["allowed_types"],
            "maintenance_id": None  # Will be filled later
        })
    return berths

def generate_maintenance_logs(berths, n_per_berth=(1,3)):
    logs = []
    now = datetime.utcnow()
    log_id = 1
    for berth in berths:
        for _ in range(random.randint(*n_per_berth)):
            performed_at = now - timedelta(days=random.randint(5, 60))
            logs.append({
                "id": log_id,
                "berth_name": berth["name"],
                "performed_at": performed_at.isoformat(),
                "notes": random.choice(["Routine", "Crane repair", "Surface cleaning"])
            })
            log_id += 1
    return logs

def generate_vessels(berths, n=25):
    vessels = []
    now = datetime.utcnow()
    for i in range(n):
        eta = now + timedelta(hours=random.randint(1, 48))
        etd = eta + timedelta(hours=random.randint(4, 12))
        berth = random.choice(berths)
        vessels.append({
            "id": i+1,
            "actual_id": 1000+i,
            "name": f"Vessel-{i}",
            "type": random.choice(["CONTAINER", "BULK", "RORO", "TANKER"]),
            "loa_m": round(random.uniform(180, 300), 1),
            "beam_m": round(random.uniform(20, 40), 1),
            "draft_m": round(random.uniform(8, 14), 1),
            "dwt_t": round(random.uniform(20000, 120000), 1),
            "eta": eta.isoformat(),
            "ebt": (eta + timedelta(hours=1)).isoformat()
        })
    return vessels

def generate_schedule_entries(vessels, berths):
    entries = []
    for i, vessel in enumerate(vessels):
        berth = random.choice(berths)
        start_time = datetime.fromisoformat(vessel["eta"]) + timedelta(minutes=random.randint(0, 60))
        end_time = start_time + timedelta(hours=random.randint(4, 12))
        entries.append({
            "id": i+1,
            "schedule_id": 1,
            "berth_id": berth["id"],
            "vessel_id": vessel["id"],
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        })
    return entries

def main():
    berths = generate_berths()
    maintenance_logs = generate_maintenance_logs(berths)
    # Assign random maintenance_id to berths
    for berth in berths:
        logs_for_berth = [log for log in maintenance_logs if log["berth_name"] == berth["name"]]
        berth["maintenance_id"] = logs_for_berth[-1]["id"] if logs_for_berth else None

    weather = generate_weather()
    vessels = generate_vessels(berths)
    schedule_entries = generate_schedule_entries(vessels, berths)

    data = {
        "weather": weather,
        "berths": berths,
        "maintenance_logs": maintenance_logs,
        "vessels": vessels,
        "schedule_entries": schedule_entries
    }
    with open("mock_data.json", "w") as f:
        json.dump(data, f, indent=2, default=str)
    print("✅ mock_data.json generated.")

if __name__ == "__main__":
    main()
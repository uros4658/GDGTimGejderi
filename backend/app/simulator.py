from .models import Vessel, Berth
from datetime import datetime, timedelta
import random

def parse_time(ts):
    if isinstance(ts, str):
        return datetime.fromisoformat(ts)
    return ts

def simulate_arrival(eta, weather):
    delay = 0
    if weather == "storm":
        delay = random.randint(20, 60)  # minutes
    elif weather == "wind":
        delay = random.randint(10, 30)
    return parse_time(eta) + timedelta(minutes=delay), delay

def simulate_vessel_event(vessel, berth_plan, berth_info, weather):
    vessel_id = vessel["id"]
    eta = parse_time(vessel["eta"])
    etd = parse_time(vessel["etd"])
    draft = vessel["draft"]

    # Assigned berth plan
    plan = berth_plan.get(vessel_id)
    if not plan:
        return {"vessel_id": vessel_id, "status": "no_plan"}

    berth = plan["berth"]
    plan_start = parse_time(plan["start_time"])
    plan_end = parse_time(plan["end_time"])

    berth_data = berth_info.get(berth)
    if not berth_data:
        return {"vessel_id": vessel_id, "status": "invalid_berth"}

    # Check berth depth compatibility
    if draft > berth_data["depth"]:
        return {
            "vessel_id": vessel_id,
            "status": "rejected_depth_too_shallow",
            "berth": berth
        }

    # Simulate delay due to weather
    actual_arrival, delay = simulate_arrival(eta, weather)

    # Calculate whether vessel is late for slot
    if actual_arrival > plan_end:
        return {
            "vessel_id": vessel_id,
            "status": "missed_slot_due_to_delay",
            "scheduled_start": plan_start,
            "actual_arrival": actual_arrival,
            "delay_minutes": delay,
            "berth": berth
        }

    # Adjusted docking start if late
    docking_start = max(actual_arrival, plan_start)
    docking_duration = (plan_end - plan_start)
    docking_end = docking_start + docking_duration

    return {
        "vessel_id": vessel_id,
        "status": "docked",
        "berth": berth,
        "scheduled_start": plan_start,
        "scheduled_end": plan_end,
        "actual_start": docking_start,
        "actual_end": docking_end,
        "delay_minutes": delay
    }

def simulate_schedule(vessels, berth_plan, berth_info, weather="calm"):
    return [
        simulate_vessel_event(v, berth_plan, berth_info, weather)
        for v in vessels
    ]

from fastapi import APIRouter
from uuid import uuid4
from random import choice, randint, uniform
from datetime import datetime, timedelta

router = APIRouter(prefix="/mockPlan", tags=["mockPlan"])

vessel_types = ["CONTAINER", "RORO", "BULK", "TANKER", "OTHER"]
berth_ids = ["A1", "B2", "C3", "D4"]

def random_berth_plan(eta):
    start = eta + timedelta(hours=randint(0, 2))
    end = start + timedelta(hours=randint(6, 18))
    return {
        "berthId": choice(berth_ids),
        "start": start.isoformat(),
        "end": end.isoformat(),
    }

@router.get("", summary="Get mock berth plan with 100 vessels")
def get_mock_plan():
    now = datetime.utcnow()
    vessels = []
    for i in range(100):
        eta = now + timedelta(hours=randint(1, 240))
        vessel = {
            "id": str(uuid4()),
            "vessel": {
                "imo": 9000000 + i,
                "name": f"Mock Ship {i}",
                "type": choice(vessel_types),
                "loa_m": round(uniform(180, 400), 1),
                "beam_m": round(uniform(25, 60), 1),
                "draft_m": round(uniform(8, 16), 1),
                "eta": eta.isoformat(),
            },
            "optimizerPlan": random_berth_plan(eta),
        }
        # Optionally add aiPrediction
        if i % 3 != 0:
            vessel["aiPrediction"] = {
                "modelVersion": "v1.0.0",
                "willChange": bool(i % 2),
                "confidence": round(uniform(0.5, 0.99), 2),
                "suggestedPlan": random_berth_plan(eta),
            }
        # Optionally add humanPlan
        if i % 4 == 0:
            vessel["humanPlan"] = random_berth_plan(eta)
        # Optionally add actualExecution
        if i % 5 == 0:
            vessel["actualExecution"] = {
                "berthId": choice(berth_ids),
                "ata": (eta + timedelta(hours=randint(0, 2))).isoformat(),
                "atd": (eta + timedelta(hours=randint(6, 24))).isoformat(),
            }
        vessels.append(vessel)
    return vessels
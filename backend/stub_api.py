# stub_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from datetime import datetime, timedelta

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic models that match your JSON schema ----------
class BerthPlan(BaseModel):
    berthId: str
    start: datetime
    end: datetime

class Vessel(BaseModel):
    imo: int
    name: str
    type: str
    loa_m: float
    beam_m: float
    draft_m: float
    eta: datetime

class VesselCall(BaseModel):
    id: str
    vessel: Vessel
    optimizerPlan: BerthPlan

# --- Hard-coded list used by both /vessels and POST /vessels
DB: list[VesselCall] = []

def seed():
    now = datetime.utcnow()
    for i in range(3):
        DB.append(
            VesselCall(
                id=str(uuid4()),
                vessel=Vessel(
                    imo=9000000 + i,
                    name=f"Mock Ship {i}",
                    type="CONTAINER",
                    loa_m=300,
                    beam_m=45,
                    draft_m=12,
                    eta=now + timedelta(hours=6 * i),
                ),
                optimizerPlan=BerthPlan(
                    berthId="B04",
                    start=now + timedelta(hours=6 * i),
                    end=now + timedelta(hours=6 * i + 8),
                ),
            )
        )

seed()

@app.get("/vessels", response_model=list[VesselCall])
def list_vessels():
    return DB

@app.post("/vessels", response_model=VesselCall)
def create_vessel(call: VesselCall):
    DB.append(call)
    return call

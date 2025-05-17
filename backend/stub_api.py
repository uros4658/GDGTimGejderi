from __future__ import annotations

import asyncio, json
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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


class AiPrediction(BaseModel):
    modelVersion: str
    willChange: bool
    confidence: Optional[float] = None
    suggestedPlan: Optional[BerthPlan] = None


class ActualExecution(BaseModel):
    berthId: str
    ata: datetime
    atd: datetime


class VesselCall(BaseModel):
    id: Optional[str] = None
    vessel: Vessel
    optimizerPlan: BerthPlan
    aiPrediction: Optional[AiPrediction] = None
    humanPlan: Optional[BerthPlan] = None
    actualExecution: Optional[ActualExecution] = None

DB: List[VesselCall] = []


def seed() -> None:
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
                aiPrediction=AiPrediction(
                    modelVersion="v1.0.0",
                    willChange=bool(i % 2),
                    confidence=0.85,
                    suggestedPlan=BerthPlan(
                        berthId="B05",
                        start=now + timedelta(hours=6 * i + 1),
                        end=now + timedelta(hours=6 * i + 9),
                    ),
                ),
            )
        )


seed()

event_queue: "asyncio.Queue[str]" = asyncio.Queue()


async def broadcast(call: VesselCall) -> None:
    """Push a JSON line to all EventSource subscribers."""
    await event_queue.put(f"data: {call.model_dump_json()}\n\n")

@app.get("/vessels", response_model=list[VesselCall])
async def list_vessels() -> list[VesselCall]:
    return DB


@app.post("/vessels", response_model=VesselCall)
async def create_vessel(call: VesselCall) -> VesselCall:
    call.id = call.id or str(uuid4())
    DB.append(call)
    await broadcast(call)
    return call


@app.get("/stream/vessels")
async def stream_vessels():
    async def event_generator():
     
        for row in DB:
            yield f"data: {row.model_dump_json()}\n\n"
     
        while True:
            data = await event_queue.get()
            yield data

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/predict")
async def predict(body: dict):
   
    call_id = body["id"]
    call = next(c for c in DB if c.id == call_id)
    will_change = call.vessel.imo % 2 == 1
    confidence = 0.87
    return {"willChange": will_change, "confidence": confidence}
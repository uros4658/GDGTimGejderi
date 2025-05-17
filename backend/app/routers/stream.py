from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import VesselCall
from datetime import datetime
import asyncio
import json

router = APIRouter(prefix="/stream", tags=["streaming"])

def vesselcall_to_schema(call: VesselCall):
    return {
        "id": str(call.id),
        "vessel": {
            "imo": call.imo,
            "name": call.vessel_name,
            "type": call.vessel_type,
            "loa_m": call.loa_m,
            "beam_m": call.beam_m,
            "draft_m": call.draft_m,
            "eta": call.eta.isoformat() if call.eta else None,
        },
        "optimizerPlan": {
            "berthId": call.optimizer_berth_id,
            "start": call.optimizer_start.isoformat() if call.optimizer_start else None,
            "end": call.optimizer_end.isoformat() if call.optimizer_end else None,
        },
        "aiPrediction": (
            {
                "modelVersion": call.ai_model_version,
                "willChange": call.ai_will_change,
                **(
                    {"confidence": call.ai_confidence}
                    if call.ai_confidence is not None
                    else {}
                ),
                "suggestedPlan": (
                    {
                        "berthId": call.ai_suggested_berth_id,
                        "start": call.ai_suggested_start.isoformat() if call.ai_suggested_start else None,
                        "end": call.ai_suggested_end.isoformat() if call.ai_suggested_end else None,
                    }
                    if call.ai_suggested_berth_id
                    else None
                ),
            }
            if call.ai_model_version and call.ai_will_change is not None
            else None
        ),
        "humanPlan": (
            {
                "berthId": call.human_berth_id,
                "start": call.human_start.isoformat() if call.human_start else None,
                "end": call.human_end.isoformat() if call.human_end else None,
            }
            if call.human_berth_id
            else None
        ),
        "actualExecution": (
            {
                "berthId": call.actual_berth_id,
                "ata": call.ata.isoformat() if call.ata else None,
                "atd": call.atd.isoformat() if call.atd else None,
            }
            if call.actual_berth_id
            else None
        ),
    }

async def vessel_stream_generator():
    last_created_at = datetime.min

    while True:
        await asyncio.sleep(2)
        with SessionLocal() as db:
            new_calls = (
                db.query(VesselCall)
                .filter(VesselCall.created_at > last_created_at)
                .order_by(VesselCall.created_at)
                .all()
            )
            for call in new_calls:
                last_created_at = call.created_at
                payload = vesselcall_to_schema(call)
                yield f"data: {json.dumps(payload)}\n\n"

@router.get("/vessels")
async def stream_vessels(request: Request):
    return StreamingResponse(vessel_stream_generator(), media_type="text/event-stream")
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import VesselCall
from datetime import datetime
import asyncio
import json

router = APIRouter(prefix="/stream", tags=["streaming"])

async def vessel_stream_generator():
    last_sent_id = 0
    while True:
        await asyncio.sleep(2)
        with SessionLocal() as db:
            db.expire_on_commit = False  # Optional, disables expiration
            # Set autocommit for read-only
            db.connection(execution_options={"isolation_level": "AUTOCOMMIT"})
            new_calls = db.query(VesselCall).filter(VesselCall.id > last_sent_id).order_by(VesselCall.id).all()
            for call in new_calls:
                last_sent_id = call.id
                yield f"data: {json.dumps({k: str(v) for k, v in call.__dict__.items() if not k.startswith('_')})}\n\n"
                
@router.get("/vessels")
async def stream_vessels(request: Request):
    return StreamingResponse(vessel_stream_generator(), media_type="text/event-stream")

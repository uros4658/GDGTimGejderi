from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import VesselCall
from datetime import datetime

router = APIRouter(prefix="/vessels", tags=["vessels"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def list_vessels(db: Session = Depends(get_db)):
    return db.query(VesselCall).order_by(VesselCall.created_at.desc()).limit(20).all()


@router.get("/{vessel_id}")
def get_vessel(vessel_id: int, db: Session = Depends(get_db)):
    vessel = db.query(VesselCall).get(vessel_id)
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")
    return vessel


@router.post("")
def create_vessel(payload: dict, db: Session = Depends(get_db)):
    vessel = VesselCall(
        imo=payload["imo"],
        vessel_name=payload.get("vessel_name"),
        vessel_type=payload.get("vessel_type"),
        loa_m=payload.get("loa_m"),
        beam_m=payload.get("beam_m"),
        draft_m=payload.get("draft_m"),
        eta=datetime.fromisoformat(payload["eta"]),
        etd=datetime.fromisoformat(payload["etd"]),
        optimizer_berth_id=payload.get("optimizer_berth_id"),
        optimizer_start=datetime.fromisoformat(payload["optimizer_start"]),
        optimizer_end=datetime.fromisoformat(payload["optimizer_end"]),
        created_at=datetime.utcnow()
    )
    db.add(vessel)
    db.commit()
    db.refresh(vessel)
    return vessel

@router.patch("/{vessel_id}/human-plan")
def override_plan(vessel_id: int, payload: dict, db: Session = Depends(get_db)):
    vessel = db.query(VesselCall).get(vessel_id)
    if not vessel:
        raise HTTPException(status_code=404, detail="Not found")
    
    vessel.human_berth_id = payload.get("human_berth_id")
    vessel.human_start = datetime.fromisoformat(payload["human_start"])
    vessel.human_end = datetime.fromisoformat(payload["human_end"])
    db.commit()
    return {"status": "updated", "id": vessel_id}

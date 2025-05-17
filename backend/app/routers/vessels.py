from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Vessel
from datetime import datetime

router = APIRouter(prefix="/vessels", tags=["vessels"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.get("")
# def list_vessels(db: Session = Depends(get_db)):
#     return db.query(VesselCall).order_by(VesselCall.created_at.desc()).limit(20).all()

@router.get("")
def list_vessels(db: Session = Depends(get_db)):
    latest_actual_id = db.query(Vessel.actual_id).order_by(Vessel.actual_id.desc()).first()
    if latest_actual_id is None:
        raise HTTPException(status_code=404, detail="No vessels found")
    return db.query(Vessel).filter(Vessel.actual_id == latest_actual_id[0]).all()

@router.get("/{actual_id}")
def get_vessel(vessel_id: int, db: Session = Depends(get_db)):
    return db.query(Vessel).filter(Vessel.actual_id == vessel_id).all()


@router.post("")
def create_vessel(payload: dict, db: Session = Depends(get_db)):
    vessel = Vessel(
        actual_id=payload["actual_id"],
        name=payload["name"],
        type=payload["type"],
        loa_m=payload["loa_m"],
        beam_m=payload["beam_m"],
        draft_m=payload["draft_m"],
        eta=payload["eta"],
        dwt_t=payload["dwt_t"]
    )
    db.add(vessel)
    db.commit()
    db.refresh(vessel)
    return vessel

@router.patch("/{actual_id}/human-plan")
def override_plan(vessel_id: int, payload: dict, db: Session = Depends(get_db)):
    vessel = db.query(Vessel).filter(Vessel.actual_id == vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")
    
    # Update the vessel's plan with the provided payload
    for key, value in payload.items():
        setattr(vessel, key, value)
    
    db.commit()
    db.refresh(vessel)
    return vessel
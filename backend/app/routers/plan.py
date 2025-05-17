from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Vessel, Weather, Berth, PredictionScheduleEntry
import app.planner as planner
from app.planner import schedule_vessels

router = APIRouter(prefix="/plan", tags=["plan"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def plan(db: Session = Depends(get_db)):
    latest_actual_id = db.query(Vessel.actual_id).order_by(Vessel.actual_id.desc()).first()
    if latest_actual_id is None:
        raise HTTPException(status_code=404, detail="No vessels found")

    vessels = []
    for v in db.query(Vessel).filter(Vessel.actual_id == latest_actual_id[0]).all():
        vessels.append(planner.Vessel(
            id=v.id,
            actual_id=v.actual_id,
            name=v.name,
            type=v.type,
            loa_m=v.loa_m,
            beam_m=v.beam_m,
            draft_m=v.draft_m,
            eta=v.eta,
            est_berth_time=v.ebt,
            dwt=v.dwt_t,
        ))
    weather = []
    for w in db.query(Weather).all():
        weather.append(planner.Weather(
            id = w.id,
            timestamp=w.timestamp,
            condition=w.condition,
            temperature_c=w.temperature_c,
            wind_speed_knots=w.wind_speed_knots,
            tide_height_m=w.tide_height_m,
        ))
    berths = []
    for b in db.query(Berth).all():
        last_maintenance_time = db.query(Weather).filter(Weather.id == b.maintenance_id).first()
        berths.append(planner.Berth(
            id = b.id,
            name = b.name,
            depth_m = b.depth_m,
            max_loa = b.max_loa,
            max_beam = b.max_beam,
            max_draft = b.max_draft,
            max_dwt = b.max_dwt,
            allowed_types = b.allowed_types,
            last_maintenance = last_maintenance_time.timestamp if last_maintenance_time else None,
        ))

    schedule = planner.schedule_vessels(berths, vessels, weather[0])
    
    schedule_entries = []
    for entry in schedule.get_schedule():
        schedule_entries.append(PredictionScheduleEntry(
            vessel_id=entry.vessel.id,
            start_time=entry.start_time,
            end_time=entry.end_time,
            berth_id=entry.berth.id
        ))

    return {"schedule": schedule_entries}
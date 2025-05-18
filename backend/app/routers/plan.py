from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Vessel, Weather, Berth, PredictionScheduleEntry, HumanFix
import app.planner as planner
from app.planner import VesselScheduleEntry
import datetime

router = APIRouter(prefix="/plan", tags=["plan"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_plan(db: Session, actual_id: int):
    vessels = []
    for v in db.query(Vessel).filter(Vessel.actual_id == actual_id).all():
        est_berth_time = datetime.timedelta(minutes=v.ebt)
        vessels.append(planner.Vessel(
            id=v.id,
            actual_id=v.actual_id,
            name=v.name,
            type=v.type,
            loa_m=v.loa_m,
            beam_m=v.beam_m,
            draft_m=v.draft_m,
            eta=v.eta,
            est_berth_time=est_berth_time,
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


    planner.model = planner.Model(berths, vessels, weather[0])
    schedule = planner.model.schedule()
    
    schedule_entries = []
    for entry in schedule.get_schedule():
        schedule_entries.append(PredictionScheduleEntry(
            vessel_id=entry.vessel.id,
            start_time=entry.start_time,
            end_time=entry.end_time,
            berth_id=entry.berth.id
        ))

    return {"schedule": schedule_entries}

@router.get("")
def plan(db: Session = Depends(get_db)):
    latest_actual_id = db.query(Vessel.actual_id).order_by(Vessel.actual_id.desc()).first()
    if latest_actual_id is None:
        raise HTTPException(status_code=404, detail="No vessels found")
    return get_plan(db, latest_actual_id[0])

@router.get("/{actual_id}")
def get_plan_by_id(actual_id: int, db: Session = Depends(get_db)):
    return get_plan(db, actual_id)

@router.patch("/human-fix")
def override_plan_body(payload: dict, db: Session = Depends(get_db)):
    actual_id = db.query(Vessel.actual_id).order_by(Vessel.actual_id.desc()).first()
    if not actual_id:
        raise HTTPException(status_code=400, detail="actual_id is required in payload")
    if not planner.model:
        raise HTTPException(status_code=500, detail="Model not initialized")

    schedule = db.query(PredictionScheduleEntry).filter(PredictionScheduleEntry.actual_id == actual_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if "changes" not in payload:
        raise HTTPException(status_code=400, detail="No changes provided")

    changes = []

    # add human fix to db
    human_fix = HumanFix(
        fix_batch_id=actual_id,
        vessel_id=payload["vessel_id"],
        berth_id=payload["berth_id"],
        start_time=payload["start_time"],
        end_time=payload["end_time"]
    )

    for planning_change in payload["changes"]:
        entry = db.query(PredictionScheduleEntry).filter(PredictionScheduleEntry.id == planning_change["id"]).first()
        if not entry:
            raise HTTPException(status_code=404, detail=f"Planning entry {planning_change['id']} not found")

        old = entry
        new = entry.copy()
        for key, value in planning_change.items():
            setattr(new, key, value)

        changes.append({
            "old": VesselScheduleEntry(
                vessel=old.vessel,
                start_time=old.start_time,
                end_time=old.end_time,
                berth=old.berth
            ),
            "new": VesselScheduleEntry(
                vessel=new.vessel,
                start_time=new.start_time,
                end_time=new.end_time,
                berth=new.berth
            )
        })

    planner.model.human_schedule_fix(actual_id, changes)

    return {}

@router.patch("/{actual_id}/human-fix")
def override_plan(actual_id: int, payload: dict, db: Session = Depends(get_db)):
    if not planner.model:
        raise HTTPException(status_code=500, detail="Model not initialized")

    schedule = db.query(PredictionScheduleEntry).filter(PredictionScheduleEntry.actual_id == actual_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if "changes" not in payload:
        raise HTTPException(status_code=400, detail="No changes provided")

    changes = []

    # add human fix to db
    human_fix = HumanFix(
        fix_batch_id=actual_id,
        vessel_id=payload["vessel_id"],
        berth_id=payload["berth_id"],
        start_time=payload["start_time"],
        end_time=payload["end_time"]
    )

    for planning_change in payload["changes"]:
        entry = db.query(PredictionScheduleEntry).filter(PredictionScheduleEntry.id == planning_change["id"]).first()
        if not entry:
            raise HTTPException(status_code=404, detail=f"Planning entry {planning_change['id']} not found")

        old = entry
        new = entry.copy()
        for key, value in planning_change.items():
            setattr(new, key, value)

        changes.append({
            "old": VesselScheduleEntry(
                vessel=old.vessel,
                start_time=old.start_time,
                end_time=old.end_time,
                berth=old.berth
            ),
            "new": VesselScheduleEntry(
                vessel=new.vessel,
                start_time=new.start_time,
                end_time=new.end_time,
                berth=new.berth
            )
        })

    planner.model.human_schedule_fix(actual_id, changes)

    return {}
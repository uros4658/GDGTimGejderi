from fastapi import APIRouter, Depends, HTTPException
import copy
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
        last_maintenance_time = b.last_maintenance
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
            berth_id=entry.berth.id,
            actual_start_time=entry.start_time,
            actual_end_time=entry.end_time,
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

@router.post("")
def create_plan(payload: dict, db: Session = Depends(get_db)):
    latest_actual_id = db.query(Vessel.actual_id).order_by(Vessel.actual_id.desc()).first()
    if latest_actual_id is None:
        raise HTTPException(status_code=404, detail="No vessels found")
    next_actual_id = latest_actual_id[0] + 1

    schedule = planner.Schedule()
    for entry in payload["schedule"]:
        vessel = db.query(Vessel).filter(Vessel.id == entry["vessel_id"]).first()
        berth = db.query(Berth).filter(Berth.id == entry["berth_id"]).first()
        if not vessel or not berth:
            raise HTTPException(status_code=404, detail="Vessel or Berth not found")

        schedule.add_entry(planner.VesselScheduleEntry(
            vessel=planner.Vessel(
                id=vessel.id,
                actual_id=vessel.actual_id,
                name=vessel.name,
                type=vessel.type,
                loa_m=vessel.loa_m,
                beam_m=vessel.beam_m,
                draft_m=vessel.draft_m,
                eta=vessel.eta,
                est_berth_time=vessel.ebt,
                dwt=vessel.dwt_t,
            ),
            start_time=entry["start_time"],
            end_time=entry["end_time"],
            berth=planner.Berth(
                id=berth.id,
                name=berth.name,
                depth_m=berth.depth_m,
                max_loa=berth.max_loa,
                max_beam=berth.max_beam,
                max_draft=berth.max_draft,
                max_dwt=berth.max_dwt,
                allowed_types=berth.allowed_types,
                last_maintenance=berth.last_maintenance
            )
        ))


@router.patch("/human-fix")
def override_plan_body(payload: dict, db: Session = Depends(get_db)):
    actual_id = db.query(Vessel.actual_id).order_by(Vessel.actual_id.desc()).first()
    if not planner.model:
        latest_actual_id = db.query(Vessel.actual_id).order_by(Vessel.actual_id.desc()).first()
        if latest_actual_id is None:
            raise HTTPException(status_code=404, detail="No vessels found")
        get_plan(db, latest_actual_id[0])

    changes = []

    # # add human fix to db
    # human_fix = HumanFix(
    #     fix_batch_id=actual_id,
    #     vessel_id=payload["vessel_id"],
    #     berth_id=payload["berth_id"],
    #     start_time=payload["start_time"],
    #     end_time=payload["end_time"]
    # )

    for planning_change in payload["changes"]:
        entry = db.query(PredictionScheduleEntry).filter(PredictionScheduleEntry.id == planning_change["id"]).first()
        if not entry:
            raise HTTPException(status_code=404, detail=f"Planning entry {planning_change['id']} not found")

        old = entry
        new = copy.deepcopy(entry)
        for key, value in planning_change.items():
            setattr(new, key, value)

        oldvessel = db.query(Vessel).filter(Vessel.id == old.vessel_id).first()
        oldberth = db.query(Berth).filter(Berth.id == old.berth_id).first()
        newvessel = db.query(Vessel).filter(Vessel.id == new.vessel_id).first()
        newberth = db.query(Berth).filter(Berth.id == new.berth_id).first()
        changes.append({
            "old": VesselScheduleEntry(
                vessel=planner.Vessel(
                    id=oldvessel.id,
                    actual_id=oldvessel.actual_id,
                    name=oldvessel.name,
                    type=oldvessel.type,
                    loa_m=oldvessel.loa_m,
                    beam_m=oldvessel.beam_m,
                    draft_m=oldvessel.draft_m,
                    eta=oldvessel.eta,
                    est_berth_time=oldvessel.ebt,
                    dwt=oldvessel.dwt_t,
                ),
                start_time=old.start_time,
                end_time=old.end_time,
                berth=planner.Berth(
                    id=oldberth.id,
                    name=oldberth.name,
                    depth_m=oldberth.depth_m,
                    max_loa=oldberth.max_loa,
                    max_beam=oldberth.max_beam,
                    max_draft=oldberth.max_draft,
                    max_dwt=oldberth.max_dwt,
                    allowed_types=oldberth.allowed_types,
                    last_maintenance=oldberth.last_maintenance
                )
            ),
            "new": VesselScheduleEntry(
                vessel=planner.Vessel(
                    id=newvessel.id,
                    actual_id=newvessel.actual_id,
                    name=newvessel.name,
                    type=newvessel.type,
                    loa_m=newvessel.loa_m,
                    beam_m=newvessel.beam_m,
                    draft_m=newvessel.draft_m,
                    eta=newvessel.eta,
                    est_berth_time=newvessel.ebt,
                    dwt=newvessel.dwt_t,
                ),
                start_time=new.start_time,
                end_time=new.end_time,
                berth=planner.Berth(
                    id=newberth.id,
                    name=newberth.name,
                    depth_m=newberth.depth_m,
                    max_loa=newberth.max_loa,
                    max_beam=newberth.max_beam,
                    max_draft=newberth.max_draft,
                    max_dwt=newberth.max_dwt,
                    allowed_types=newberth.allowed_types,
                    last_maintenance=newberth.last_maintenance
                )
            )
        })

    planner.model.human_schedule_fix(actual_id, changes)

    return {}

@router.patch("/{actual_id}/human-fix")
def override_plan(actual_id: int, payload: dict, db: Session = Depends(get_db)):
    if not planner.model:
        latest_actual_id = db.query(Vessel.actual_id).order_by(Vessel.actual_id.desc()).first()
        if latest_actual_id is None:
            raise HTTPException(status_code=404, detail="No vessels found")
        get_plan(db, latest_actual_id[0])

    schedule = db.query(PredictionScheduleEntry).filter(PredictionScheduleEntry.actual_id == actual_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if "changes" not in payload:
        raise HTTPException(status_code=400, detail="No changes provided")

    changes = []

    # # add human fix to db
    # human_fix = HumanFix(
    #     fix_batch_id=actual_id,
    #     vessel_id=payload["vessel_id"],
    #     berth_id=payload["berth_id"],
    #     start_time=payload["start_time"],
    #     end_time=payload["end_time"]
    # )

    for planning_change in payload["changes"]:
        entry = db.query(PredictionScheduleEntry).filter(PredictionScheduleEntry.id == planning_change["id"]).first()
        if not entry:
            raise HTTPException(status_code=404, detail=f"Planning entry {planning_change['id']} not found")

        old = entry
        new = copy.deepcopy(entry)
        for key, value in planning_change.items():
            setattr(new, key, value)

        try:
            db.add(new)
            db.commit()
            db.refresh(new)
        finally:
            db.close()

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
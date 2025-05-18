import datetime
from typing import List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from app.db import SessionLocal
from app.models import PredictionLog, PredictionScheduleEntry


class Berth:
    def __init__(self, id: str, name: str, depth_m: float, max_loa: float, max_beam: float, 
                 max_draft: float, max_dwt: float, allowed_types: List[str], last_maintenance: Optional[datetime.datetime]):
        self.id = id
        self.name = name
        self.depth_m = depth_m
        self.max_loa = max_loa
        self.max_beam = max_beam
        self.max_draft = max_draft
        self.max_dwt = max_dwt
        self.allowed_types = allowed_types
        self.last_maintenance = last_maintenance

    def __str__(self):
        return f"Berth: {self.name}, Depth: {self.depth_m}m, Max LOA: {self.max_loa}m, Max Beam: {self.max_beam}m, Max Draft: {self.max_draft}m, Max DWT: {self.max_dwt}t, Allowed Types: {', '.join(self.allowed_types)}, Last Maintenance: {self.last_maintenance}"

    def __repr__(self):
        return f"Berth(id={self.id}, name='{self.name}', depth_m={self.depth_m}, max_loa={self.max_loa}, max_beam={self.max_beam}, max_draft={self.max_draft}, max_dwt={self.max_dwt}, allowed_types={self.allowed_types}, last_maintenance={self.last_maintenance})"

    def is_suitable_for_vessel(self, vessel: 'Vessel') -> bool:
        return (self.max_loa >= vessel.loa_m and
                self.max_beam >= vessel.beam_m and
                self.max_draft >= vessel.draft_m and
                vessel.type in self.allowed_types)

class Vessel:
    def __init__(self, id: int, actual_id: int, name: str, type: str, loa_m: float, beam_m: float,
                 draft_m: float, eta: datetime.datetime, est_berth_time: datetime.timedelta, dwt: float):
        self.id = id
        self.name = name
        self.type = type
        self.loa_m = loa_m
        self.beam_m = beam_m
        self.draft_m = draft_m
        self.eta = eta
        self.est_berth_time = est_berth_time
        self.actual_id = actual_id
        self.dwt_t = dwt

    def __str__(self):
        return f"Vessel: {self.name}, Type: {self.type}, LOA: {self.loa_m}m, Beam: {self.beam_m}m, Draft: {self.draft_m}m, ETA: {self.eta}, Estimated Berth Time: {self.est_berth_time}"

    def __repr__(self):
        return f"Vessel(id={self.id}, name='{self.name}', type='{self.type}', loa_m={self.loa_m}, beam_m={self.beam_m}, draft_m={self.draft_m}, eta={self.eta}, est_berth_time={self.est_berth_time}, actual_id={self.actual_id}, dwt_t={self.dwt_t})"

class VesselScheduleEntry:

    def __init__(self, vessel: Vessel, start_time: datetime.datetime, end_time: datetime.datetime, berth: Berth):
        self.vessel = vessel
        self.start_time = start_time
        self.end_time = end_time
        self.berth = berth
        
    def __str__(self):
        return f"Vessel: {self.vessel.name}, Start Time: {self.start_time}, End Time: {self.end_time}, Berth: {self.berth.name}"

    def __repr__(self):
        return f"VesselScheduleEntry(vessel={self.vessel}, start_time={self.start_time}, end_time={self.end_time}, berth={self.berth})"

class Weather:
    def __init__(self, id: int, timestamp: datetime.datetime, condition: str, temperature_c: float,
                 wind_speed_knots: float, tide_height_m: float):
        self.id = id
        self.timestamp = timestamp
        self.condition = condition
        self.temperature_c = temperature_c
        self.wind_speed_knots = wind_speed_knots
        self.tide_height_m = tide_height_m

    def __str__(self):
        return f"Weather: {self.condition}, Temperature: {self.temperature_c}°C, Wind Speed: {self.wind_speed_knots} knots, Tide Height: {self.tide_height_m}m"

    def __repr__(self):
        return f"Weather(id={self.id}, timestamp={self.timestamp}, condition='{self.condition}', temperature_c={self.temperature_c}, wind_speed_knots={self.wind_speed_knots}, tide_height_m={self.tide_height_m})"

class Schedule:
    def __init__(self):
        self.entries: List[VesselScheduleEntry] = []

    def add_entry(self, entry: VesselScheduleEntry):
        self.entries.append(entry)

    def get_schedule(self) -> List[VesselScheduleEntry]:
        return self.entries

    def __str__(self):
        return "\n".join(str(entry) for entry in self.entries)

    def __repr__(self):
        return f"Schedule(entries={self.entries})"

def schedule_fcfs(berths: List[Berth], vessels: List[Vessel], weather: Weather) -> Schedule:
    schedule = Schedule()
    for vessel in vessels:
        for berth in berths:
            if berth.is_suitable_for_vessel(vessel):
                # check if berth available at time
                for entry in schedule.get_schedule():
                    if berth.id == entry.vessel.id and not (entry.end_time < vessel.eta or entry.start_time > vessel.eta + vessel.est_berth_time):
                        break
                start_time = max(vessel.eta, datetime.datetime.now())
                end_time = start_time + vessel.est_berth_time
                schedule.add_entry(VesselScheduleEntry(vessel, start_time, end_time, berth))
                break
    return schedule

# linear regression model for improving berth allocation
def train_model(data: pd.DataFrame) -> Tuple[float,LinearRegression]:
    X = data[['max_loa', 'max_beam', 'max_draft', 'max_dwt']]
    y = data['est_berth_time']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Model Mean Squared Error: {mse}")
    return (mse, model)

def predict_berth_time(model: LinearRegression, berth: Berth, vessel: Vessel) -> float:
    features = np.array([[berth.max_loa, berth.max_beam, berth.max_draft, berth.max_dwt]])
    est_berth_time = model.predict(features)
    return est_berth_time[0]

class Model:
    def __init__(self, berths: List[Berth], vessels: List[Vessel], weather: Weather):
        self.berths = berths
        self.vessels = vessels
        self.weather = weather
        self.model: Optional[LinearRegression] = None

    def schedule(self) -> Schedule:
        # get schedule from the db
        db = SessionLocal()
        try:
            latest_actual_id = db.query(PredictionScheduleEntry.actual_id).order_by(PredictionScheduleEntry.actual_id.desc()).first()
            if latest_actual_id is None:
                raise Exception("No vessels found")
            schedule = Schedule()
            for entry in db.query(PredictionScheduleEntry).filter(PredictionScheduleEntry.actual_id == latest_actual_id[0]).all():
                vessel = Vessel(
                    id=entry.vessel_id,
                    actual_id=entry.actual_id,
                    name="",
                    type="",
                    loa_m=0,
                    beam_m=0,
                    draft_m=0,
                    eta=entry.start_time,
                    est_berth_time=entry.end_time - entry.start_time,
                    dwt=0
                )
                berth = Berth(
                    id=entry.berth_id,
                    name="",
                    depth_m=0,
                    max_loa=0,
                    max_beam=0,
                    max_draft=0,
                    max_dwt=0,
                    allowed_types=[],
                    last_maintenance=None
                )
                schedule.add_entry(VesselScheduleEntry(vessel, entry.start_time, entry.end_time, berth))
            return schedule
        finally:
            db.close()


        # return schedule_fcfs(self.berths, self.vessels, self.weather)
        # if self.model is None:
        #     return schedule_fcfs(self.berths, self.vessels, self.weather)

        # model = self.model
        # schedule = Schedule()
        # for vessel in self.vessels:
        #     for berth in self.berths:
        #         if berth.is_suitable_for_vessel(vessel):
        #             est_berth_time = predict_berth_time(model, berth, vessel)
        #             # check if berth available at time
        #             for entry in schedule.get_schedule():
        #                 if berth.id == entry.vessel.id and not (entry.end_time < vessel.eta or entry.start_time > vessel.eta + datetime.timedelta(hours=est_berth_time)):
        #                     break
        #             start_time = max(vessel.eta, datetime.datetime.now())
        #             end_time = start_time + datetime.timedelta(hours=est_berth_time)
        #             schedule.add_entry(VesselScheduleEntry(vessel, start_time, end_time, berth))
        #             break
        # return schedule

    def human_schedule_fix(self, actual_id: int, fixes: List[Tuple[VesselScheduleEntry, VesselScheduleEntry]]):
        for fix in fixes:
            original_entry, new_entry = fix
            berth_data = pd.DataFrame({
                'max_loa': [berth.max_loa for berth in self.berths],
                'max_beam': [berth.max_beam for berth in self.berths],
                'max_draft': [berth.max_draft for berth in self.berths],
                'max_dwt': [berth.max_dwt for berth in self.berths],
                'est_berth_time': [1000] * len(self.berths),  # Placeholder for actual est_berth_time
            })
            (mse, self.model) = train_model(berth_data)
            db = SessionLocal()
            try:
                log_entry = PredictionLog(error=mse, actual_id=actual_id[0])
                db.add(log_entry)
                db.commit()
                db.refresh(log_entry)
            finally:
                db.close()

model: Optional[Model] = None
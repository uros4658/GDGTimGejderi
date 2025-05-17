import datetime
from typing import List, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class Berth:
    def __init__(self, id: str, name: str, width: float, max_loa: float,
                 max_beam: float, max_draft: float, max_dwt: int, allowed_types: List[str],
                 last_maintenance: Optional[datetime.datetime] = None):
        self.id = id
        self.name = name
        self.width = width
        self.max_loa = max_loa
        self.max_beam = max_beam
        self.max_draft = max_draft
        self.max_dwt = max_dwt
        self.allowed_types = allowed_types
        self.last_maintenance = last_maintenance
        self.available = True

    def __str__(self):
        return f"Berth: {self.name}, Width: {self.width}m, Max LOA: {self.max_loa}m, Max Beam: {self.max_beam}m, Max Draft: {self.max_draft}m, Max DWT: {self.max_dwt}, Available: {self.available}"

    def __repr__(self):
        return f"Berth(id='{self.id}', name='{self.name}', width={self.width}, max_loa={self.max_loa}, max_beam={self.max_beam}, max_draft={self.max_draft}, max_dwt={self.max_dwt}, allowed_types={self.allowed_types}, last_maintenance={self.last_maintenance})"

    def is_suitable_for_vessel(self, vessel: 'Vessel') -> bool:
        return (self.max_loa >= vessel.loa_m and
                self.max_beam >= vessel.beam_m and
                self.max_draft >= vessel.draft_m and
                vessel.type in self.allowed_types)

class Vessel:
    def __init__(self, id: str, name: str, type: str, width: float, loa_m: float, beam_m: float,
                 draft_m: float, eta: datetime.datetime, est_berth_time: datetime.timedelta):
        self.id = id
        self.name = name
        self.type = type
        self.width = width
        self.loa_m = loa_m
        self.beam_m = beam_m
        self.draft_m = draft_m
        self.eta = eta
        self.est_berth_time = est_berth_time

    def __str__(self):
        return f"Vessel: {self.name}, Type: {self.type}, Width: {self.width}m, LOA: {self.loa_m}m, Beam: {self.beam_m}m, Draft: {self.draft_m}m, ETA: {self.eta}, Est. Berth Time: {self.est_berth_time}"

    def __repr__(self):
        return f"Vessel(id='{self.id}', name='{self.name}', type='{self.type}', width={self.width}, loa_m={self.loa_m}, beam_m={self.beam_m}, draft_m={self.draft_m}, eta={self.eta}, est_berth_time={self.est_berth_time})"

class VesselScheduleEntry:
    def __init__(self, vessel: 'Vessel', start_time: datetime.datetime, end_time: datetime.datetime, berth: 'Berth' = None):
        self.vessel = vessel
        self.start_time = start_time
        self.end_time = end_time
        self.berth = berth
        
    def __str__(self):
        return f"Vessel: {self.vessel.name}, Start: {self.start_time}, End: {self.end_time}, Berth: {self.berth.name if self.berth else None}"

    def __repr__(self):
        return f"VesselScheduleEntry(vessel={self.vessel}, start_time={self.start_time}, end_time={self.end_time}, berth={self.berth})"

class Conditions:
    def __init__(self, wind_speed: float, wave_height: float, visibility: float):
        self.wind_speed = wind_speed
        self.wave_height = wave_height
        self.visibility = visibility

    def __str__(self):
        return f"Conditions: Wind Speed: {self.wind_speed}m/s, Wave Height: {self.wave_height}m, Visibility: {self.visibility}km"

    def __repr__(self):
        return f"Conditions(wind_speed={self.wind_speed}, wave_height={self.wave_height}, visibility={self.visibility})"

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

def schedule_fcfs(berths: List[Berth], vessels: List[Vessel], conditions: Conditions) -> Schedule:
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
def train_model(data: pd.DataFrame) -> LinearRegression:
    X = data[['width', 'max_loa', 'max_beam', 'max_draft', 'max_dwt']]
    y = data['est_berth_time']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Model MSE: {mse}")
    return model

def predict_berth_time(model: LinearRegression, berth: Berth, vessel: Vessel) -> float:
    features = np.array([[berth.width, berth.max_loa, berth.max_beam, berth.max_draft, berth.max_dwt]])
    est_berth_time = model.predict(features)
    return est_berth_time[0]

def schedule_with_model(berths: List[Berth], vessels: List[Vessel], conditions: Conditions, model: LinearRegression) -> Schedule:
    schedule = Schedule()
    for vessel in vessels:
        for berth in berths:
            if berth.is_suitable_for_vessel(vessel):
                est_berth_time = predict_berth_time(model, berth, vessel)
                # check if berth available at time
                for entry in schedule.get_schedule():
                    if berth.id == entry.vessel.id and not (entry.end_time < vessel.eta or entry.start_time > vessel.eta + datetime.timedelta(hours=est_berth_time)):
                        break
                start_time = max(vessel.eta, datetime.datetime.now())
                end_time = start_time + datetime.timedelta(hours=est_berth_time)
                schedule.add_entry(VesselScheduleEntry(vessel, start_time, end_time, berth))
                break
    return schedule

# # import csv
# berth_data = pd.read_csv('MOCK_BERTH.csv')
# vessel_data = pd.read_csv('MOCK_VESSEL.csv')
# conditions_data = pd.read_csv('MOCK_CONDITIONS.csv')

# # create berth objects
# berths = []
# for index, row in berth_data.iterrows():
#     berth = Berth(
#         id=row['id'],
#         name=row['name'],
#         width=row['width'],
#         max_loa=row['max_loa'],
#         max_beam=row['max_beam'],
#         max_draft=row['max_draft'],
#         max_dwt=row['max_dwt'],
#         allowed_types=row['allowed_types'].split(','),
#         last_maintenance=pd.to_datetime(row['last_maintenance']) if pd.notna(row['last_maintenance']) else None
#     )
#     berths.append(berth)

# # create vessel objects
# vessels = []

# for index, row in vessel_data.iterrows():
#     vessel = Vessel(
#         id=row['id'],
#         name=row['name'],
#         type=row['type'],
#         width=row['width'],
#         loa_m=row['loa_m'],
#         beam_m=row['beam_m'],
#         draft_m=row['draft_m'],
#         eta=pd.to_datetime(row['eta']),
#         est_berth_time=pd.to_timedelta(row['est_berth_time'])
#     )
#     vessels.append(vessel)

# conditions = Conditions(
#     wind_speed=conditions_data['wind_speed'].iloc[0],
#     wave_height=conditions_data['wave_height'].iloc[0],
#     visibility=conditions_data['visibility'].iloc[0]
# )

# generate mock data

berth_data = pd.DataFrame({
    'id': ['B2', 'B3'],  # Removed 'B1'
    'name': ['Berth 2', 'Berth 3'],
    'width': [25.0, 30.0],
    'max_loa': [250.0, 300.0],
    'max_beam': [35.0, 40.0],
    'max_draft': [12.0, 15.0],
    'max_dwt': [60000, 70000],
    'allowed_types': ['Bulk', 'General Cargo'],
    'last_maintenance': [None, None],
    'est_berth_time': [6.0, 7.0]  # Mock estimated berth times in hours
})
vessel_data = pd.DataFrame({
    'id': ['V1', 'V2', 'V3'],
    'name': ['Vessel 1', 'Vessel 2', 'Vessel 3'],
    'type': ['Container', 'Bulk', 'General Cargo'],
    'width': [15.0, 20.0, 25.0],
    'loa_m': [150.0, 200.0, 250.0],
    'beam_m': [20.0, 25.0, 30.0],
    'draft_m': [8.0, 10.0, 12.0],
    'eta': [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(3)],
    'est_berth_time': [datetime.timedelta(hours=5), datetime.timedelta(hours=6), datetime.timedelta(hours=7)]
})
conditions_data = pd.DataFrame({
    'wind_speed': [5.0],
    'wave_height': [1.0],
    'visibility': [10.0]
})
# create berth objects
berths = []
for index, row in berth_data.iterrows():
    berth = Berth(
        id=row['id'],
        name=row['name'],
        width=row['width'],
        max_loa=row['max_loa'],
        max_beam=row['max_beam'],
        max_draft=row['max_draft'],
        max_dwt=row['max_dwt'],
        allowed_types=row['allowed_types'].split(','),
        last_maintenance=pd.to_datetime(row['last_maintenance']) if pd.notna(row['last_maintenance']) else None
    )
    berths.append(berth)
# create vessel objects
vessels = []
for index, row in vessel_data.iterrows():
    vessel = Vessel(
        id=row['id'],
        name=row['name'],
        type=row['type'],
        width=row['width'],
        loa_m=row['loa_m'],
        beam_m=row['beam_m'],
        draft_m=row['draft_m'],
        eta=pd.to_datetime(row['eta']),
        est_berth_time=pd.to_timedelta(row['est_berth_time'])
    )
    vessels.append(vessel)
conditions = Conditions(
    wind_speed=conditions_data['wind_speed'].iloc[0],
    wave_height=conditions_data['wave_height'].iloc[0],
    visibility=conditions_data['visibility'].iloc[0]
)


schedule_fcfs_result = schedule_fcfs(berths, vessels, conditions)

model = train_model(berth_data)
schedule_model_result = schedule_with_model(berths, vessels, conditions, model)
print("FCFS Schedule:")
print(schedule_fcfs_result)
print("\nModel Schedule:")
print(schedule_model_result)


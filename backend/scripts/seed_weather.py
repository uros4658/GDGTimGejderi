from random import choices, uniform
from datetime import datetime, timedelta
from app.models import Weather
from app.db import SessionLocal

session = SessionLocal()

base_time = datetime(2025, 7, 1, 0, 0)  # summer
conditions = ["CLEAR", "RAIN", "STORM"]
weights = [0.7, 0.2, 0.1]  # more clear in summer

for hour in range(72):  # 3 days
    ts = base_time + timedelta(hours=hour)
    condition = choices(conditions, weights)[0]
    session.add(Weather(
        timestamp=ts,
        condition=condition,
        temperature_c=uniform(25, 34),
        wind_speed_knots=uniform(2, 15),
        tide_height_m=uniform(0.8, 1.8)
    ))

session.commit()
session.close()

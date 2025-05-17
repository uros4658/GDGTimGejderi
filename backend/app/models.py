from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from app.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String
from app.db import Base

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True, nullable=False)  # Weather time
    condition = Column(String(16))  # e.g. CLEAR, RAIN, STORM
    temperature_c = Column(Float)
    wind_speed_knots = Column(Float)
    tide_height_m = Column(Float)

class VesselCall(Base):
    __tablename__ = "vessel_calls"
    id = Column(Integer, primary_key=True)
    imo = Column(Integer, index=True)  # Changed to Integer for IMO
    vessel_name = Column(String(64))
    vessel_type = Column(String(16))
    loa_m = Column(Float)
    beam_m = Column(Float)
    draft_m = Column(Float)
    eta = Column(DateTime, nullable=False)
    optimizer_berth_id = Column(String)
    optimizer_start = Column(DateTime)
    optimizer_end = Column(DateTime)
    ai_model_version = Column(String)
    ai_will_change = Column(Boolean)
    ai_confidence = Column(Float)
    ai_suggested_berth_id = Column(String)
    ai_suggested_start = Column(DateTime)
    ai_suggested_end = Column(DateTime)
    human_berth_id = Column(String)
    human_start = Column(DateTime)
    human_end = Column(DateTime)
    actual_berth_id = Column(String)
    ata = Column(DateTime)
    atd = Column(DateTime)
    etd = Column(DateTime, nullable=False)
    planned_berth = Column(String)
    human_override = Column(String)
    actual_berth = Column(String)
    predicted_change = Column(Boolean, default=False)
    prediction_confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    ata = Column(DateTime)              # Actual Time of Arrival
    aba = Column(DateTime)              # Actual Berthing Assignment time
    weather_id = Column(Integer, ForeignKey("weather.id"))


class Berth(Base):
    __tablename__ = "berths"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    length_m = Column(Float)
    depth_m = Column(Float)

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True)
    vessel_call_id = Column(Integer, ForeignKey("vessel_calls.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    will_change = Column(Boolean)
    confidence = Column(Float)
    model_version = Column(String)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    
class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"
    id = Column(Integer, primary_key=True)
    berth_name = Column(String, ForeignKey("berths.name"))
    performed_at = Column(DateTime)
    notes = Column(String)
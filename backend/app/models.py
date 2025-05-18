from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Sequence
from app.db import Base
from datetime import datetime
from app.db import Base

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True, nullable=False)  # Weather time
    condition = Column(String(16))  # e.g. CLEAR, RAIN, STORM
    temperature_c = Column(Float)
    wind_speed_knots = Column(Float)
    tide_height_m = Column(Float)

class Vessel(Base):
    __tablename__ = "vessels"
    id = Column(Integer, primary_key=True)
    actual_id = Column(Integer, Sequence("vessel_id_seq"), nullable=False)
    name = Column(String(64))
    type = Column(String(16))
    loa_m = Column(Float)
    beam_m = Column(Float)
    draft_m = Column(Float)
    dwt_t = Column(Float)
    eta = Column(DateTime, nullable=False)
    ebt = Column(Integer) # estimated berth time in minutes

class Berth(Base):
    __tablename__ = "berths"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    depth_m = Column(Float)
    max_loa = Column(Float) # length overall
    max_beam = Column(Float) # width overall
    max_draft = Column(Float)
    max_dwt = Column(Float)
    allowed_types = Column(String)
    last_maintenance = Column(DateTime)

class PredictionScheduleEntry(Base):
    __tablename__ = "vessel_schedule_entries"
    id = Column(Integer, primary_key=True)
    actual_id = Column(Integer, ForeignKey("vessels.actual_id"))
    berth_id = Column(Integer, ForeignKey("berths.id"))
    vessel_id = Column(Integer, ForeignKey("vessels.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    schedule_id = Column(Integer)
    actual_start_time = Column(DateTime)
    actual_end_time = Column(DateTime)
    actual_arrival_time = Column(DateTime)

class HumanFix(Base):
    __tablename__ = "human_fixes"
    id = Column(Integer, primary_key=True)
    actual_id = Column(Integer, ForeignKey("vessels.actual_id"))
    vessel_id = Column(Integer, ForeignKey("vessels.id"))
    berth_id = Column(Integer, ForeignKey("berths.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True)
    actual_id = Column(Integer, ForeignKey("vessels.actual_id"))
    timestamp = Column(DateTime, default=datetime.now())
    error = Column(Float, nullable=False)
    
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
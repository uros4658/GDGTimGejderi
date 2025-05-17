from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
<<<<<<< HEAD
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:miskopisko@uros:5432/simulationData")
=======

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:miskopisko@localhost:5432/simulationData")
>>>>>>> b3a1f48e160972920a099721338278fafb7e3141

# Set echo to False to reduce SQL log noise
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
from fastapi import FastAPI
from app.db import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "OK"}
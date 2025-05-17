from fastapi import FastAPI
from app.models import Base
from app.db import engine
from app.routers import vessels

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(vessels.router)

@app.get("/")
def root():
    return {"status": "ok"}

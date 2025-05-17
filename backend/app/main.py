from fastapi import FastAPI
from app.models import Base
from app.db import engine
from app.routers import vessels
from app.routers import stream
from app.routers import metrics
from app.routers import retrain
from fastapi.routing import APIRouter
from app.middleware.auth import APIKeyRoute
from app.routers import auth
from app.routers import mockBerthPlan

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(vessels.router)
app.include_router(stream.router)
app.include_router(metrics.router)
app.include_router(retrain.router)
app.include_router(auth.router)
app.include_router(mockBerthPlan.router)
app.router.route_class = APIKeyRoute


@app.get("/")
def root():
    return {"status": "ok"}

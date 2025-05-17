from fastapi import FastAPI
from app.models import Base
from app.db import engine
from app.routers import vessels
from app.routers import metrics
from app.routers import plan
from fastapi.routing import APIRouter
from app.middleware.auth import APIKeyRoute
from app.routers import auth
from app.routers import mockBerthPlan
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_methods=["*"],        
    allow_headers=["*"],       
    allow_credentials=False,    
)
Base.metadata.create_all(bind=engine)
app.include_router(vessels.router)
app.include_router(metrics.router)
app.include_router(plan.router)
app.include_router(auth.router)
app.include_router(mockBerthPlan.router)
app.router.route_class = APIKeyRoute


@app.get("/")
def root():
    return {"status": "ok"}

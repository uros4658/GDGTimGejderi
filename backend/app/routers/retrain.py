from fastapi import APIRouter, BackgroundTasks
import subprocess

router = APIRouter(prefix="/retrain", tags=["retrain"])

def run_training():
    subprocess.run(["make", "train"], cwd="backend")

@router.post("/")
def trigger_retrain(bg: BackgroundTasks):
    bg.add_task(run_training)
    return {"status": "retraining started"}

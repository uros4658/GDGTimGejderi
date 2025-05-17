from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get():
    data = {
        "imo": 9387422,
        "vessel_name": "Test Ship",
        "vessel_type": "BULK",
        "loa_m": 200,
        "beam_m": 32,
        "draft_m": 11.1,
        "eta": "2025-05-18T08:00:00Z",
        "etd": "2025-05-18T18:00:00Z",
        "optimizer_berth_id": "C1",
        "optimizer_start": "2025-05-18T07:30:00Z",
        "optimizer_end": "2025-05-18T18:30:00Z"
    }
    r = client.post("/vessels", json=data)
    assert r.status_code == 200
    payload = r.json()
    assert payload["imo"] == 9387422

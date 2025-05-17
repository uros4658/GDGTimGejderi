def test_metrics():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)

    r = client.get("/metrics/24h")
    assert r.status_code == 200
    assert "accuracy" in r.json()

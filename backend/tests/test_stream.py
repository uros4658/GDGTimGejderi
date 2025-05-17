def test_stream_vessels():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    with client.stream("GET", "/stream/vessels") as r:
        for line in r.iter_lines():
            if line:
                assert "data:" in line
                break

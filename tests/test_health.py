from fastapi.testclient import TestClient

from app.cmd.public_api import fastapi_app

client = TestClient(fastapi_app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

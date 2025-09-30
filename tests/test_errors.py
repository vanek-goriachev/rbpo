from fastapi.testclient import TestClient

from app.cmd.public_api import fastapi_app

client = TestClient(fastapi_app)


def test_not_found_item():
    r = client.get("/post/105358d1-106e-4a18-afa3-db745afdffda")
    assert r.status_code == 404
    body = r.json()
    assert "error" in body and body["error"]["code"] == "not_found"


def test_validation_error():
    r = client.get("/post/34151345", params={"name": ""})
    assert r.status_code == 422

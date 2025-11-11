from fastapi.testclient import TestClient

from app.cmd.public_api import fastapi_app

client = TestClient(fastapi_app)


def test_create_post_greenpath():
    response = client.post(
        "/post",
        json={
            "title": "My awesome post",
            "body": "This is the content of my awesome post.",
            "user_id": 1,
        },
    )
    assert response.status_code == 200

    response = client.get(f"/post/{response.json()['id']}")
    assert response.json()["title"] == "My awesome post"
    assert response.json()["body"] == "This is the content of my awesome post."


def test_create_post_title_too_long():
    long_title = "a" * 256
    response = client.post(
        "/post", json={"title": long_title, "body": "Some body text", "user_id": 1}
    )
    assert response.status_code == 400
    assert "Title must be at most 255 characters" in response.json()["error"]


def test_create_post_body_too_long():
    long_body = "a" * 4096
    response = client.post("/post", json={"title": "Short title", "body": long_body, "user_id": 1})
    assert response.status_code == 400
    assert "Body must be at most 4095 characters" in response.json()["error"]


def test_create_post_sql_injection_attempt():
    title = "'; DROP TABLE posts;--"
    response = client.post("/post", json={"title": title, "body": "Some body text", "user_id": 1})
    assert response.status_code == 400
    assert "Title must be at most 255 characters" in response.json()["error"]


def test_create_post_title_boundary_255():
    title = "a" * 255
    response = client.post("/post", json={"title": title, "body": "Some body text", "user_id": 1})
    assert response.status_code == 200

    response = client.get(f"/post/{response.json()['id']}")
    assert response.json()["title"] == title


def test_create_post_body_boundary_4095():
    body = "a" * 4095
    response = client.post("/post", json={"title": "Short title", "body": body, "user_id": 1})
    assert response.status_code == 200

    response = client.get(f"/post/{response.json()['id']}")
    assert response.json()["body"] == body

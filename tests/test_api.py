import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_user(client):
    response = client.post(
        "/register",
        json={
            "username": "pytest_user",
            "password": "testpass"
        }
    )

    assert response.status_code in [200, 400]


def test_login(client):
    response = client.post(
        "/login",
        data={
            "username": "pytest_user",
            "password": "testpass"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_current_user(client):

    login = client.post(
        "/login",
        data={
            "username": "pytest_user",
            "password": "testpass"
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "username" in response.json()


def test_non_admin_cannot_create_book(client):

    login = client.post(
        "/login",
        data={
            "username": "pytest_user",
            "password": "testpass"
        }
    )

    token = login.json()["access_token"]

    response = client.post(
        "/books/",
        json={
            "title": "Unauthorized Book",
            "author": "Someone",
            "published_year": 2024
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_invalid_book_id(client):
    response = client.get("/books/invalidid")
    assert response.status_code in [400, 404]

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def get_token(client):
    login = client.post(
        "/login",
        data={
            "username": "pytest_user",
            "password": "testpass"
        }
    )
    return login.json()["access_token"]


def test_get_books(client):

    token = get_token(client)

    response = client.get(
        "/books/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [200, 405]


def test_create_book_without_auth(client):

    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Someone",
            "published_year": 2024
        }
    )

    assert response.status_code in [401, 403]


def test_get_book_invalid_id(client):

    token = get_token(client)

    response = client.get(
        "/books/507f1f77bcf86cd799439011",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [400, 404]


def test_duplicate_registration(client):

    response = client.post(
        "/register",
        json={
            "username": "pytest_user",
            "password": "testpass"
        }
    )

    assert response.status_code in [400, 409]


def test_login_wrong_password(client):

    response = client.post(
        "/login",
        data={
            "username": "pytest_user",
            "password": "wrongpass"
        }
    )

    assert response.status_code in [400, 401, 403, 422]


    token = get_token(client)

    response = client.post(
        "/books/",
        json={"title": "Incomplete"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [400, 422]


def test_access_users_me_without_token(client):

    response = client.get("/users/me")

    assert response.status_code in [401, 403]


def test_login_missing_fields(client):

    response = client.post(
        "/login",
        data={"username": "pytest_user"}
    )

    assert response.status_code in [400, 422]


def test_register_empty_payload(client):

    response = client.post("/register", json={})

    assert response.status_code in [400, 422]


def test_invalid_token_access(client):

    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )

    assert response.status_code in [401, 403] 

def test_create_book_missing_fields(client):

    token = get_token(client)

    response = client.post(
        "/books/",
        json={"title": "Incomplete"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [400, 403, 422]


def test_access_users_me_without_token(client):

    response = client.get("/users/me")

    assert response.status_code in [401, 403]


def test_login_missing_fields(client):

    response = client.post(
        "/login",
        data={"username": "pytest_user"}
    )

    assert response.status_code in [400, 422]


def test_register_empty_payload(client):

    response = client.post("/register", json={})

    assert response.status_code in [400, 422]


def test_invalid_token_access(client):

    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )

    assert response.status_code in [401, 403]

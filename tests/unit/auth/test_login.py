import pytest
from fastapi import status
from fastapi.testclient import TestClient
from tests.conftest import client


@pytest.fixture
def test_user(client):
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "full_name": "Test User",
        "email": "test.user@example.com",
        "password": "testpass123",
    }
    response = client.post("/auth/registration/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    return user_data


def login_json(email, password):
    return {"email": email, "password": password}


def test_successful_login(client, test_user):
    response = client.post(
        "/auth/login/", json=login_json(test_user["email"], test_user["password"])
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)


def test_successful_token_login(client, test_user):
    form_data = {"username": test_user["email"], "password": test_user["password"]}
    response = client.post("/auth/login/token", data=form_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_email(client):
    response = client.post(
        "/auth/login/", json=login_json("fake@example.com", "testpass123")
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"


def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login/", json=login_json(test_user["email"], "wrongpass")
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"


def test_login_empty_fields(client):
    response = client.post("/auth/login/", json=login_json("", ""))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("missing", ["email", "password"])
def test_login_missing_fields(client, missing):
    data = {"email": "test@example.com", "password": "testpass123"}
    data.pop(missing)
    response = client.post("/auth/login/", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_invalid_email_format(client):
    response = client.post("/auth/login/", json=login_json("bad-email", "testpass123"))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_token_missing_fields(client):
    response = client.post("/auth/login/token", data={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_token_invalid_credentials(client):
    form_data = {"username": "nope@example.com", "password": "invalid"}
    response = client.post("/auth/login/token", data=form_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"

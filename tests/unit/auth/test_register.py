import pytest
from fastapi import status
from tests.conftest import client


@pytest.fixture
def valid_user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepass123",
        "phone_number": "+1234567890",
        "profile_picture": "https://example.com/profile.jpg",
    }


def test_successful_registration(client, valid_user_data):
    response = client.post("/auth/registration/", json=valid_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user"]["email"] == valid_user_data["email"]
    assert data["user"]["full_name"] == valid_user_data["full_name"]
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_registration_without_optional_fields(client):
    minimal_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "full_name": "Jane Smith",
        "email": "jane.smith@example.com",
        "password": "securepass123",
    }
    response = client.post("/auth/registration/", json=minimal_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user"]["email"] == minimal_data["email"]


def test_registration_with_invalid_email(client, valid_user_data):
    valid_user_data["email"] = "not-an-email"
    response = client.post("/auth/registration/", json=valid_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_registration_with_short_password(client, valid_user_data):
    valid_user_data["password"] = "123"
    response = client.post("/auth/registration/", json=valid_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_registration_with_existing_email(client, valid_user_data):
    client.post("/auth/registration/", json=valid_user_data)  # First registration
    response = client.post("/auth/registration/", json=valid_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered."


def test_registration_with_missing_required_fields(client):
    incomplete_data = {"first_name": "John", "email": "john@example.com"}
    response = client.post("/auth/registration/", json=incomplete_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_registration_autofill_full_name(client):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.auto@example.com",
        "password": "securepass123",
    }
    response = client.post("/auth/registration/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user"]["full_name"] == "John Doe"


@pytest.mark.parametrize(
    "field,value",
    [
        ("email", None),
        ("email", ""),
        ("email", " "),
        ("password", None),
        ("password", ""),
        ("password", " "),
        ("first_name", None),
        ("first_name", ""),
        ("first_name", " "),
        ("last_name", None),
        ("last_name", ""),
        ("last_name", " "),
    ],
)
def test_registration_with_empty_fields(client, valid_user_data, field, value):
    data = valid_user_data.copy()
    if value is None:
        data.pop(field, None)
    else:
        data[field] = value

    response = client.post("/auth/registration/", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_registration_token_creation_failure(client, mocker, valid_user_data):
    mocker.patch(
        "api.v1.auth.routes.register.generate_access_token",
        side_effect=Exception("Token generation failed."),
    )
    response = client.post("/auth/registration/", json=valid_user_data)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == "Token creation failed."

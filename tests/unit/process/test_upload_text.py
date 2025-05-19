import pytest
from unittest.mock import patch
from tests.conftest import client

from main import app
from db.models.chatbot.chatbot import Chatbot
from api.v1.chatbots.routes.chat import get_current_user


@pytest.fixture
def headers():
    return {"Authorization": "Bearer faketoken"}


@pytest.fixture
def valid_text_input():
    return {
        "chatbot_id": 1,
        "file_name": "test_text",
        "text": "This is a test text content",
    }


@pytest.fixture
def override_user():
    return type("User", (), {"id": 1})()


def override_get_current_user():
    return type("User", (), {"id": 1})()


def reset_overrides():
    app.dependency_overrides.clear()


@patch("api.v1.process.routes.upload.upload_text.embedding_pipeline")
@patch("api.v1.process.routes.upload.upload_text.create_data_source")
def test_successful_text_upload(
    mock_create_data_source,
    mock_embedding,
    db_session,
    client,
    headers,
    valid_text_input,
):
    chatbot = Chatbot(user_id=1, name="TestBot", description="test description")
    db_session.add(chatbot)
    db_session.commit()

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.post("/process/text", json=valid_text_input, headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Text uploaded successfully",
        "chatbot_id": 1,
        "file_name": "test_text",
        "text": valid_text_input["text"],
    }

    reset_overrides()


def test_text_upload_without_authentication(client, valid_text_input):
    response = client.post("/process/text", json=valid_text_input)
    assert response.status_code == 401


def test_text_upload_with_nonexistent_chatbot(db_session, client, headers):
    app.dependency_overrides[get_current_user] = override_get_current_user

    invalid_input = {
        "chatbot_id": 99999,
        "file_name": "test_text",
        "text": "This is a test text content",
    }

    response = client.post("/process/text", json=invalid_input, headers=headers)

    assert response.status_code == 404
    assert "Chatbot not found" in response.json()["detail"]

    reset_overrides()

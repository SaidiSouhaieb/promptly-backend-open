import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch, AsyncMock
from main import app
from api.v1.chatbots.routes.chat import get_current_user


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def headers():
    return {"Authorization": "Bearer faketoken"}


@pytest.fixture
def chat_input():
    return {
        "chatbot_id": 123,
        "text": "Hello, how are you?",
        "model_name": "mistral7b",
    }


@pytest.fixture
def override_user():
    return type("User", (), {"id": 1})()


def override_get_current_user():
    return type("User", (), {"id": 1})()


def reset_overrides():
    app.dependency_overrides.clear()


@patch("api.v1.chatbots.routes.chat.get_chatbot_and_data_source")
@patch("api.v1.chatbots.routes.chat.generate_response", new_callable=AsyncMock)
def test_successful_chat(
    mock_generate_response, mock_get_data, client, headers, chat_input
):
    app.dependency_overrides[get_current_user] = override_get_current_user

    chatbot = type("Chatbot", (), {"user_id": 1})()
    mock_get_data.return_value = (chatbot, object())
    mock_generate_response.return_value = "Mocked reply"

    response = client.post("/chatbots/chat", json=chat_input, headers=headers)

    assert response.status_code == 200
    assert response.json()["reply"] == "Mocked reply"
    reset_overrides()


def test_chat_without_authentication(client, chat_input):
    response = client.post("/chatbots/chat", json=chat_input)
    assert response.status_code == 401


@patch("utils.auth.jwt_handler.generate_access_token")
def test_chat_with_invalid_token(mock_generate_token, client, chat_input):
    mock_generate_token.side_effect = Exception("Invalid token")

    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/chatbots/chat", json=chat_input, headers=headers)

    assert response.status_code == 401


@patch("api.v1.chatbots.routes.chat.get_chatbot_and_data_source")
def test_chat_with_nonexistent_chatbot(mock_get_data, client, headers, chat_input):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_get_data.side_effect = HTTPException(
        status_code=404, detail="Chatbot not found"
    )

    response = client.post("/chatbots/chat", json=chat_input, headers=headers)

    assert response.status_code == 404
    assert "Chatbot not found" in response.json()["detail"]
    reset_overrides()


@patch("api.v1.chatbots.routes.chat.get_chatbot_and_data_source")
def test_chat_with_unauthorized_chatbot(mock_get_data, client, headers, chat_input):
    app.dependency_overrides[get_current_user] = override_get_current_user

    unauthorized_chatbot = type("Chatbot", (), {"user_id": 2})()  # Current user is id=1
    mock_get_data.return_value = (unauthorized_chatbot, object())

    response = client.post("/chatbots/chat", json=chat_input, headers=headers)

    assert response.status_code == 403
    reset_overrides()


@patch("api.v1.chatbots.routes.chat.get_chatbot_and_data_source")
@patch("api.v1.chatbots.routes.chat.generate_response", new_callable=AsyncMock)
def test_chat_with_generation_error(
    mock_generate_response, mock_get_data, client, headers, chat_input
):
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_get_data.return_value = (type("Chatbot", (), {"user_id": 1})(), object())
    mock_generate_response.side_effect = ValueError("Failed to generate response")

    response = client.post("/chatbots/chat", json=chat_input, headers=headers)

    assert response.status_code == 404
    assert "Failed to generate response" in response.json()["detail"]
    reset_overrides()

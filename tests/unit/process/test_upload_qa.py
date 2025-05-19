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
def override_user():
    return type("User", (), {"id": 1})()


@pytest.fixture
def valid_qa_input():
    return {
        "chatbot_id": 1,
        "file_name": "test_qa",
        "qa_list": [
            {"question": "Test question 1?", "answer": "Test answer 1"},
            {"question": "Test question 2?", "answer": "Test answer 2"},
        ],
    }


def override_get_current_user():
    return type("User", (), {"id": 1})()


def reset_overrides():
    app.dependency_overrides.clear()


@patch("api.v1.process.routes.upload.upload_qa.embedding_pipeline")
@patch("api.v1.process.routes.upload.upload_qa.create_data_source")
def test_successful_qa_upload(
    mock_create_data_source,
    mock_embedding,
    db_session,
    client,
    headers,
    valid_qa_input,
):
    chatbot = Chatbot(user_id=1, name="TestBot", description="test description")
    db_session.add(chatbot)
    db_session.commit()

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.post("/process/qa", json=valid_qa_input, headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "message": "File uploaded successfully",
        "chatbot_id": 1,
        "file_name": "test_qa",
        "qa_list": valid_qa_input["qa_list"],
    }

    reset_overrides()


def test_qa_upload_without_authentication(client, valid_qa_input):
    response = client.post("/process/qa", json=valid_qa_input)
    assert response.status_code == 401


def test_qa_upload_with_nonexistent_chatbot(db_session, client, headers):
    app.dependency_overrides[get_current_user] = override_get_current_user

    qa_input = {
        "chatbot_id": 99999,
        "file_name": "test_qa",
        "qa_list": [{"question": "Test question?", "answer": "Test answer"}],
    }

    response = client.post("/process/qa", json=qa_input, headers=headers)

    assert response.status_code == 404
    assert "Chatbot not found" in response.json()["detail"]

    reset_overrides()

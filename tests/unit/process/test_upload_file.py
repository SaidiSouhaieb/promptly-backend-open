import json
import pytest
from unittest.mock import patch, AsyncMock

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
def valid_upload_files():
    return {
        "upload_file": ("test.pdf", b"test content", "application/pdf"),
        "file_input": (
            None,
            json.dumps({"chatbot_id": 1, "file_name": "test_document"}),
            "application/json",
        ),
    }


def override_get_current_user():
    return type("User", (), {"id": 1})()


def reset_overrides():
    app.dependency_overrides.clear()


@patch("api.v1.process.routes.upload.upload_file.create_temp_file")
@patch("api.v1.process.routes.upload.upload_file.content_extractor")
@patch("api.v1.process.routes.upload.upload_file.embedding_pipeline")
def test_successful_file_upload(
    mock_embedding,
    mock_extractor,
    mock_temp_file,
    db_session,
    client,
    headers,
    valid_upload_files,
):
    chatbot = Chatbot(user_id=1, name="TestBot", description="Sample bot")
    db_session.add(chatbot)
    db_session.commit()

    app.dependency_overrides[get_current_user] = override_get_current_user
    mock_temp_file.return_value = "/tmp/test_file"
    mock_extractor.get_text_content.return_value = "extracted text"

    response = client.post(
        "/process/upload-file/", files=valid_upload_files, headers=headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "File uploaded successfully",
        "chatbot_id": 1,
        "file_name": "test_document",
    }

    reset_overrides()


def test_file_upload_without_authentication(client):
    files = {
        "upload_file": ("test.pdf", b"test content", "application/pdf"),
        "file_input": (
            None,
            json.dumps({"chatbot_id": 1, "file_name": "test_document"}),
            "application/json",
        ),
    }

    response = client.post("/process/upload-file/", files=files)
    assert response.status_code == 401


@patch("api.v1.process.routes.upload.upload_file.create_temp_file")
def test_file_upload_with_nonexistent_chatbot(
    mock_temp_file, db_session, client, headers
):
    app.dependency_overrides[get_current_user] = override_get_current_user

    files = {
        "upload_file": ("test.pdf", b"test content", "application/pdf"),
        "file_input": (
            None,
            json.dumps({"chatbot_id": 99999, "file_name": "test_document"}),
            "application/json",
        ),
    }

    response = client.post("/process/upload-file/", files=files, headers=headers)

    assert response.status_code == 404
    assert "Chatbot not found" in response.json()["detail"]

    reset_overrides()

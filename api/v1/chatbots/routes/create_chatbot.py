import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from core.config import settings
from db.models.user import User
from db.models.chatbot.chatbot import Chatbot
from db.session import get_db
from models.chatbot.create_chatbot import CreateChatbot, ChatbotCreationResponse
from utils.auth.password_manager import hash_password
from core.logging import logging, setup_logging
from core.security import get_current_user

setup_logging()

create_chatbot_router = APIRouter(prefix="/create-chatbot")


@create_chatbot_router.post(
    "/",
    response_model=ChatbotCreationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chatbot(
    current_user: Annotated[User, Depends(get_current_user)],
    chatbot: CreateChatbot,
    db: Annotated[Session, Depends(get_db)],
):

    new_chatbot = Chatbot(
        name=chatbot.name,
        description=chatbot.description,
        user_id=current_user.id,
    )

    try:
        db.add(new_chatbot)
        db.commit()
        db.refresh(new_chatbot)
    except Exception as e:
        db.rollback()
        logging.error(f"Chatbot creation failed: {e}")
        raise HTTPException(status_code=500, detail="Chatbot creation failed.")

    logging.info(
        f"Chatbot created successfully: {new_chatbot.name} (ID: {new_chatbot.id})"
    )

    return {
        "id": new_chatbot.id,
        "name": new_chatbot.name,
        "description": new_chatbot.description,
        "message": "Chatbot created successfully!",
    }

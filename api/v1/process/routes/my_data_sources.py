import os
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.chatbot.text_input import TextInput
from db.models.chatbot import Chatbot
from db.models.file.data_source import DataSource
from db.models.user import User
from db.session import get_db
from llms.loaders.model_loader import ModelLoader
from services.chatbot.get_chain import get_chain
from core.security import get_current_user


my_data_sources_router = APIRouter(prefix="/my-data-sources")

model_loader = ModelLoader()


@my_data_sources_router.post("/{chatbot_id}")
async def my_data_sources_endpoint(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    chatbot_id: str = "",
):
    chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not chatbot:
        return {"error": "Chatbot not found"}

    print(
        chatbot.user_id, " ", current_user.id, " ", current_user.id == chatbot.user_id
    )
    if chatbot.user_id != current_user.id:
        return {"error": "You are not authorized to access this chatbot"}
    print(chatbot_id)
    print(db.query(DataSource).all(), "dataseources\n\n")
    data_sources = (
        db.query(DataSource).filter(DataSource.chatbot_id == chatbot_id).all()
    )
    return data_sources

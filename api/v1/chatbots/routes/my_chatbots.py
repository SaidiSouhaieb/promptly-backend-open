# back/core/routes/chat.py
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.chatbot.text_input import TextInput
from db.models.chatbot import Chatbot

from db.session import get_db
from llms.loaders.model_loader import ModelLoader
from services.chatbot.get_chain import get_chain

my_chatbots_router = APIRouter(prefix="/my-chatbots")

model_loader = ModelLoader()


@my_chatbots_router.post("/")
async def my_chatbots_endpoint(db: Session = Depends(get_db)):
    chatbots = db.query(Chatbot).filter(Chatbot.user_id == 1).all()
    return chatbots

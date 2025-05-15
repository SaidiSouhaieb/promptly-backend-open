from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.models.chatbot import Chatbot
from db.models.user import User
from db.session import get_db
from core.security import get_current_user
from models.chatbot.my_chatbots import MyChatbotsResponse, Chatbot as ChatbotModel


my_chatbots_router = APIRouter(prefix="/my-chatbots")


@my_chatbots_router.post("/", response_model=MyChatbotsResponse)
async def my_chatbots_endpoint(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    chatbots = (
        db.query(Chatbot.name, Chatbot.description)
        .filter(Chatbot.user_id == current_user.id)
        .all()
    )

    if not chatbots:
        raise HTTPException(status_code=404, detail="No chatbots found for the user.")

    response_chatbots = [
        ChatbotModel(name=chatbot.name, description=chatbot.description)
        for chatbot in chatbots
    ]

    return MyChatbotsResponse(chatbots=response_chatbots)

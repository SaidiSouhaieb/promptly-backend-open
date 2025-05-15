from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models.chatbot.text_input import TextInput
from db.session import get_db
from db.models.user.user import User

from services.chatbot.chat import generate_response, get_chatbot_and_data_source
from core.security import get_current_user
from models.chatbot.chat_response import ChatResponse


chatbot_router = APIRouter(prefix="/chat")


@chatbot_router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    current_user: Annotated[User, Depends(get_current_user)],
    input: TextInput,
    db: Annotated[Session, Depends(get_db)],
):
    chatbot, data_source = get_chatbot_and_data_source(db, input.chatbot_id)

    if chatbot.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Unauthorized access to this chatbot"
        )

    try:
        reply = await generate_response(input, data_source)
        return ChatResponse(reply=reply)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

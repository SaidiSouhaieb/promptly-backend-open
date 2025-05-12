# back/core/routes/chat.py
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.chatbot.text_input import TextInput
from db.models.chatbot.message import Message
from db.session import get_db

from llms.loaders.model_loader import ModelLoader
from services.chatbot.get_chain import get_chain

from core.constants import (
    STORAGE_PATH,
    TEMP_PATH,
    VECTORSTORE_NAME,
    VECTORSTORE_TYPE,
    EMBEDDING_MODEL_NAME,
)


chatbot_router = APIRouter(prefix="/chat")

model_loader = ModelLoader()


@chatbot_router.post("/")
async def chat_endpoint(input: TextInput, db: Session = Depends(get_db)):
    db_path = os.path.join(
        STORAGE_PATH, "vectorstores", VECTORSTORE_NAME, VECTORSTORE_TYPE
    )

    print(db_path, "path\n\n\n")

    model_name = input.model_name
    qa_chain = get_chain(db_path, EMBEDDING_MODEL_NAME, model_name, input.text)
    response = qa_chain.invoke(input.text)

    return {"reply": response}

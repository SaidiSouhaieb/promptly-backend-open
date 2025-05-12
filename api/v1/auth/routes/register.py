import os

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import TextInput

from database.models.user import User
from db.session import get_db
from src.config.load_llm import ModelLoader
from models.user.register import Registration

register_router = APIRouter(prefix="/registration")

model_loader = ModelLoader()


@register_router.post("/")
async def registration(user: Registration, db: Session = Depends(get_db)):
    print(f"Received user data: {user.dict()} \n\n\n")

    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

from pydantic import BaseModel, EmailStr, constr, model_validator
from typing import Optional


class CreateChatbot(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class ChatbotCreationResponse(BaseModel):
    id: int
    name: str
    description: str
    message: str

    class Config:
        orm_mode = True

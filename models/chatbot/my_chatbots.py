from datetime import datetime
from typing import List

from pydantic import BaseModel


class Chatbot(BaseModel):
    name: str
    description: str


class MyChatbotsResponse(BaseModel):
    chatbots: List[Chatbot]

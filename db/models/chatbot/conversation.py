from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, text

from db.base import BaseModel


class Conversation(BaseModel):
    __tablename__ = "Conversation"

    id = Column(Integer, primary_key=True, nullable=False)
    chatbot_id = Column(Integer, ForeignKey("Chatbot.id"), nullable=False)
    title = Column(String, nullable=False)

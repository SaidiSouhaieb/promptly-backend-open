import enum

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Enum

from db.base import BaseModel


class SenderEnum(enum.Enum):
    user = "user"
    chatbot = "chatbot"


class Message(BaseModel):
    __tablename__ = "Message"

    id = Column(Integer, primary_key=True, nullable=False)
    conversation_id = Column(Integer, ForeignKey("Conversation.id"), nullable=True)
    sender = Column(Enum(SenderEnum), nullable=True)
    content = Column(String, nullable=False)
    token_count = Column(Integer, nullable=False)

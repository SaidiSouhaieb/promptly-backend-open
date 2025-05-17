import enum

from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey, text, Enum

from db.base import BaseModel


class LanguageEnum(enum.Enum):
    en = "English"
    ar = "Arabic"
    fr = "French"


class ChatbotSettings(BaseModel):
    __tablename__ = "ChatbotSettings"

    id = Column(Integer, primary_key=True, nullable=False)
    chatbot_id = Column(Integer, ForeignKey("Chatbot.id"), nullable=False)
    temperature = Column(Float, nullable=False, default=0.7)
    top_p = Column(Integer, nullable=False, default=1.0)
    model_name = Column(String, nullable=False)
    system_prompt = Column(String, nullable=False)
    language = Column(Enum(LanguageEnum), nullable=False)

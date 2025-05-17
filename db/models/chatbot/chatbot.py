from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship

from db.base import BaseModel


class Chatbot(BaseModel):
    __tablename__ = "Chatbot"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    user = relationship("User", backref="chatbots")

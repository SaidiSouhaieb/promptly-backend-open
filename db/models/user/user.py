from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

from db.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_premium = Column(Boolean, server_default="TRUE")

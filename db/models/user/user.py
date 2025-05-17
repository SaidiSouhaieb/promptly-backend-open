from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text
from db.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, unique=False)
    last_name = Column(String, unique=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    full_name = Column(String)
    profile_picture = Column(String, nullable=True)
    is_premium = Column(Boolean, server_default="FALSE")
    is_active = Column(Boolean, server_default="TRUE")
    is_verified = Column(Boolean, server_default="FALSE")

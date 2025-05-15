from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class Login(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

from pydantic import BaseModel, EmailStr


class Registration(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True

from pydantic import BaseModel, EmailStr, constr, model_validator
from typing import Optional


class Registration(BaseModel):
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    password: constr(min_length=6)
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None

    @model_validator(mode="before")
    def autofill_full_name(cls, data):
        data["full_name"] = f"{data['first_name']} {data['last_name']}"
        return data

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True


class RegistrationResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"

from pydantic import BaseModel, EmailStr, constr, model_validator, field_validator
from typing import Optional


class Registration(BaseModel):
    first_name: str
    last_name: str
    full_name: Optional[str] = None
    email: EmailStr
    password: constr(min_length=6)
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None

    @model_validator(mode="after")
    def autofill_full_name(cls, data):
        data.full_name = f"{data.first_name} {data.last_name}"
        return data

    @field_validator("first_name", "last_name", "password", "email", mode="before")
    @classmethod
    def not_empty(cls, v: str, info):
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} must not be empty or whitespace")
        return v

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

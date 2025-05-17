import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.config import settings
from db.models.user import User
from db.session import get_db
from models.user.register import Registration, RegistrationResponse
from utils.auth.password_manager import hash_password
from utils.auth.jwt_handler import generate_access_token
from core.logging import logging
from services.user.register_user import register_user


register_router = APIRouter(prefix="/registration")


@register_router.post(
    "/", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED
)
async def registration(user: Registration, db: Session = Depends(get_db)):
    new_user = register_user(user, db)

    try:
        access_token = generate_access_token(new_user.email)
    except Exception as e:
        logging.error(f"Token creation failed for {new_user.email}: {e}")
        raise HTTPException(status_code=500, detail="Token creation failed.")

    return {"user": new_user, "access_token": access_token, "token_type": "bearer"}

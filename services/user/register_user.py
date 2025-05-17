import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from db.models.user import User
from db.session import get_db
from models.user.register import Registration, RegistrationResponse
from utils.auth.password_manager import hash_password
from core.logging import logging


def register_user(user: Registration, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = hash_password(user.password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
        phone_number=user.phone_number,
        full_name=user.full_name,
        profile_picture=user.profile_picture,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        logging.error(f"Registration failed: {e}")
        raise HTTPException(status_code=500, detail="Registration failed.")
    return new_user

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.user import User
from utils.auth.password_manager import verify_password
from core.config import settings


def create_access_token(
    db: Session,
    credential,
    password,
) -> str:

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )


def login_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

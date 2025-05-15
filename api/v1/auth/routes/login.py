from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.models.user import User
from models.user.login import Login, Token
from db.session import get_db
from utils.auth.jwt_handler import generate_access_token
from core.config import settings
from services.user.authenticate import login_user

login_router = APIRouter(prefix="/login", tags=["Auth"])


@login_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = login_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )
    access_token = generate_access_token(email=user.email)
    return Token(access_token=access_token, token_type="bearer")


@login_router.post("/", response_model=Token, status_code=status.HTTP_200_OK)
async def login(user_data: Login, db: Session = Depends(get_db)):
    user = login_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
    )
    access_token = generate_access_token(email=user.email)
    return Token(access_token=access_token, token_type="bearer")

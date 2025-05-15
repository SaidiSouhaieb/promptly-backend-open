import jwt
from fastapi import Depends
from typing import Annotated
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from models.user.login import TokenData
from db.session import get_db
from db.models.user.user import User
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/token")


def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user

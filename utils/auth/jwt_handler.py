from datetime import datetime, timedelta, timezone
import jwt

from core.config import settings


def generate_access_token(email: str) -> str:
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires

    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

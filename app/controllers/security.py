__all__ = ["verify_password", "get_password_hash", "encode_jwt", "decode_jwt"]

from typing import Optional, Union

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from settings import JWT_SECRET_KEY, JWT_ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def encode_jwt(
        data: dict,
        expires_delta: Optional[timedelta] = None
) -> str:
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=30)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt(
        token: str
) -> Union[dict, None]:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None

__all__ = ["verify_password", "get_password_hash", "JWTToken"]

from typing import Optional, Type

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.settings import JWT_SECRET, JWT_DECODE_ALGORYTHM, JWT_ACCESS_TOKEN_EXPIRE


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class JWTToken:
    def __init__(self, token: str) -> None:
        try:
            self._data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_DECODE_ALGORYTHM])
        except JWTError:
            raise ValueError(f"Can't decode JWT token: {token}")

        self._type = self._data.get("type")
        self._expire = self._data.get("exp")
        self.subject = self._data.get("sub")

        if self._type is None or self.subject is None or self._expire is None:
            raise ValueError(f"Missing required fields in JWT token: {self._data} -> [type, sub, exp, sp]")

    @property
    def is_expired(self) -> bool:
        return datetime.utcfromtimestamp(self._expire) < datetime.utcnow()

    @property
    def is_refresh_token(self) -> bool:
        return self._type == "refresh"

    @property
    def is_access_token(self) -> bool:
        return self._type == "access"

    @classmethod
    def create_access_token(
            cls: Type["JWTToken"],
            subject: str,
            expires_delta: Optional[timedelta] = JWT_ACCESS_TOKEN_EXPIRE
    ) -> str:
        expire_time = datetime.utcnow() + expires_delta
        data = {
            "type": "access",
            "sub": subject,
            "exp": expire_time
        }
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_DECODE_ALGORYTHM)

    @classmethod
    def create_refresh_token(
            cls: Type["JWTToken"],
            subject: str,
            expires_delta: Optional[timedelta] = JWT_ACCESS_TOKEN_EXPIRE
    ) -> str:
        expire_time = datetime.utcnow() + expires_delta
        data = {
            "type": "refresh",
            "sub": subject,
            "exp": expire_time
        }
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_DECODE_ALGORYTHM)

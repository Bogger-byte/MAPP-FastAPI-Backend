__all__ = ["verify_password", "get_password_hash", "JWTToken"]

import datetime
from datetime import timedelta
from typing import Optional, Type

import jwt
from passlib.context import CryptContext

from app.settings import (
    JWT_SECRET,
    JWT_DECODE_ALGORYTHM,
    JWT_ACCESS_TOKEN_EXPIRE,
    JWT_REFRESH_TOKEN_EXPIRE
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class JWTToken:
    def __init__(
            self,
            _type: str,
            subject: str,
            issuer: str,
            expire_delta: Optional[timedelta] = None,
    ) -> None:
        self.type = _type
        self.subject = subject
        self.issuer = issuer
        if expire_delta is None:
            if _type == "access":
                expire_delta = JWT_ACCESS_TOKEN_EXPIRE
            if _type == "refresh":
                expire_delta = JWT_REFRESH_TOKEN_EXPIRE
        self.expire_delta = expire_delta

    @property
    def is_refresh_token(self) -> bool:
        return self.type == "refresh"

    @property
    def is_access_token(self) -> bool:
        return self.type == "access"

    @classmethod
    def decode(cls: Type["JWTToken"], token: str) -> "JWTToken":
        try:
            data = jwt.decode(
                token,
                JWT_SECRET,
                leeway=JWT_ACCESS_TOKEN_EXPIRE,
                algorithms=[JWT_DECODE_ALGORYTHM],
                options={"require": ["exp", "sub", "iss", "type"]}
            )
        except jwt.DecodeError or jwt.MissingRequiredClaimError:
            raise ValueError(f"Can't decode JWT token: {token}")
        except jwt.ExpiredSignatureError:
            raise ValueError(f"Token is expired")

        _type = data.get("type")
        subject = data.get("sub")
        issuer = data.get("iss")
        return cls(_type, subject, issuer)

    def encode(self) -> str:
        data = {
            "type": self.type,
            "sub": self.subject,
            "iss": self.issuer,
            "exp": datetime.datetime.utcnow() + self.expire_delta
        }
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_DECODE_ALGORYTHM)

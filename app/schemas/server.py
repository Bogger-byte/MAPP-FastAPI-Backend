__all__ = [
    "ServerCreate",
    "ServerUpdate",
    "Server",
    "ServerDatabase",
    "ServerInfo",
    "ip_validation_regex"
]

import socket
from typing import Optional, Type, Any

from pydantic import BaseModel, EmailStr, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Server


ip_validation_regex = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"


def validate_ip(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("Ip address is not string", value)
    try:
        socket.inet_aton(value)
    except OSError:
        raise ValueError("Invalid ip address", value)
    else:
        return value


class ServerCreate(BaseModel):
    name: str
    host: str
    secret: str
    email: EmailStr

    @validator("host")
    def validate_ip(cls: Type["ServerCreate"], v: Any) -> str:
        return validate_ip(v)


class ServerUpdate(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None
    secret: Optional[str] = None
    email: Optional[EmailStr] = None

    @validator("host")
    def validate_ip(cls: Type["ServerUpdate"], v: Any) -> str:
        return validate_ip(v)


ServerDatabase = pydantic_model_creator(
    Server, name="ServerDB"
)


Server = pydantic_model_creator(
    Server, name="Server"
)


class ServerInfo(BaseModel):
    is_enabled: bool
    players_online: int

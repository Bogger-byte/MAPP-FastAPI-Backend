__all__ = ["ip_validation_regex", "ServerCreate", "ServerUpdate", "Server", "ServerDatabase"]

from typing import Optional, Type, Any

import re
from pydantic import BaseModel, EmailStr, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from models import Server


ip_validation_regex = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'


def validate_ip(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Ip address is not string")
    regex = re.compile(ip_validation_regex, re.I)
    match = regex.match(value)
    if not bool(match):
        raise ValueError("Invalid ip address")
    return value


class ServerCreate(BaseModel):
    name: str
    host: str
    api_key: str
    email: EmailStr

    @validator("host")
    def validate_ip(cls: Type["ServerCreate"], v: Any) -> str:
        return validate_ip(v)


class ServerUpdate(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None
    api_key: Optional[str] = None
    email: Optional[EmailStr] = None

    @validator("host")
    def validate_ip(cls: Type["ServerUpdate"], v: Any) -> str:
        return validate_ip(v)


ServerDatabase = pydantic_model_creator(
    Server, name="ServerDB"
)
Server = pydantic_model_creator(
    Server, name="Server", exclude=("key", "created_at", "modified_at")
)

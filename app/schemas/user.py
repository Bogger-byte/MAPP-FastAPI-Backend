__all__ = ["UserCreate", "UserUpdate", "UserDatabase", "User"]

from typing import Optional

from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from pydantic import EmailStr

from models import User


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None


UserDatabase = pydantic_model_creator(
    User, name="UserDB"
)


User = pydantic_model_creator(
    User, name="User", exclude=("password", "created_at", "modified_at")
)


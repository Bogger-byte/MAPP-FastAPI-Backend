__all__ = ["CredentialsValidationForm", "Scopes"]

from enum import Enum
from typing import Optional, Type, Union

from fastapi import Form, HTTPException, status


class Scopes(Enum):
    DEFAULT_USER = "DEFAULT_USER"
    MINECRAFT_SERVER = "MINECRAFT_SERVER"

    @classmethod
    def value_of(cls: Type["Scopes"], scope_str: str) -> Union[Type["Scopes"], None]:
        return cls.__members__.get(scope_str)

    @classmethod
    def dict(cls) -> dict[str, str]:
        return {scope.name: scope.value for scope in cls}


class CredentialsValidationForm:
    def __init__(
            self,
            grant_type: str = Form(None, regex="password"),
            username: Optional[str] = Form(...),
            password: Optional[str] = Form(...),
            scope: str = Form(...),
            client_id: Optional[str] = Form(default=""),
            client_secret: Optional[str] = Form(default="")
    ) -> None:
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret

        if [scope for scope in self.scopes if Scopes.value_of(scope) is None]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type of scope {self.scopes} -> [{Scopes.dict()}]"
            )
        if Scopes.DEFAULT_USER in self.scopes and self.client_id is None and self.client_secret is None:
            return
        if Scopes.MINECRAFT_SERVER in self.scopes and (self.client_id is None or self.client_secret is None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough arguments"
            )

__all__ = ["CredentialsValidationForm", "Scopes"]

from enum import Enum
from typing import Optional, Type, Union

from fastapi import Form


class Scopes(Enum):
    SUPER_USER = "super-user"
    DEFAULT_USER = "default-user"
    MINECRAFT_SERVER = "minecraft-server"

    @classmethod
    def value_of(cls: Type["Scopes"], scope_str: str) -> Union[Type["Scopes"], None]:
        return {scope.value: scope for scope in cls}.get(scope_str)

    @classmethod
    def dict(cls: Type["Scopes"]) -> dict[str, str]:
        return {scope.value: scope.value for scope in cls}


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
            raise ValueError(f"Invalid type of scope {self.scopes} -> [{Scopes.dict()}]")

        if Scopes.DEFAULT_USER in self.scopes and self.client_id is None and self.client_secret is None:
            return
        if Scopes.MINECRAFT_SERVER in self.scopes and (self.client_id is None or self.client_secret is None):
            raise ValueError(f"Not enough arguments")

__all__ = ["StandartPermissions", "ClientPermissions"]

from enum import Enum
import re
from itertools import zip_longest
from typing import Optional, Union


class ClientPermissions:
    def __init__(
            self,
            issuer: str,
            endpoints: Union[tuple[str, ...], str],
            extends: Optional[tuple] = None
    ) -> None:
        self.issuer = issuer
        self.endpoints = endpoints
        if isinstance(self.endpoints, tuple) and extends is not None:
            self.endpoints += extends[1]

    @staticmethod
    def _routes_equal(match_url: str, url: str) -> bool:
        match_folders = match_url.split("/")
        folders = url.split("/")
        for match_folder, folder in zip_longest(match_folders, folders, fillvalue=None):
            if match_folder is None or folder is None:
                return False
            if re.search("{\w+}", match_folder) is not None:
                continue
            if match_folder != folder:
                return False
        return True

    @staticmethod
    def deserialize(
            serialized_perms: str
    ) -> "ClientPermissions":
        issuer, packed_endpoints = serialized_perms.split("=")
        routes = "All" if packed_endpoints == "All" else packed_endpoints.split(";")
        return ClientPermissions(issuer, routes)

    def serialize(
            self
    ) -> str:
        packed_routes = "All" if self.endpoints == "All" else ";".join(map(str, self.endpoints))
        return f"{self.issuer}={packed_routes}"

    def is_permitted_to(
            self,
            method: str,
            path: str
    ) -> bool:
        if self.endpoints == "All":
            return True
        route = f"{method}:{path}"
        return bool([endpoint for endpoint in self.endpoints
                     if self._routes_equal(endpoint, route)])


class StandartPermissions(Enum):
    def __new__(
            cls,
            issuer: str,
            endpoints: tuple[str, ...],
            extends: Optional[ClientPermissions] = None
    ) -> "StandartPermissions":
        obj = object.__new__(cls)
        obj.permissions = ClientPermissions(
            issuer=issuer,
            endpoints=endpoints,
            extends=extends
        )
        return obj

    BASIC = (
        "BASIC", (
            "POST:/api/oauth/jwt/token",
            "POST:/api/oauth/jwt/refresh",
            "GET:/api/users/{id}",
            "GET:/api/servers/{id}",
            "GET:/api/servers/{id}/info",
            "GET:/api/servers/{id}/players-data",
            "GET:/api/servers/{id}/regions",
            "GET:/api/servers/{id}/regions/{world}/{x}/{z}",
            "WS:servers_info",
            "WS:server_data"
        )
    )
    SERVER = (
        "SERVER", (
            "GET:/api/servers/me",
            "UPDATE:/api/servers/me",
            "DELETE:/api/servers/me",
            "POST:/api/servers/me/players-data",
            "POST:/api/servers/me/regions",
            "POST:/api/servers/me/info",
        ),
        BASIC
    )
    USER = (
        "USER", (
            "GET:/api/users/me",
            "UPDATE:/api/users/me",
            "DELETE:/api/users/me",
            "POST:/api/servers/register",
            "POST:/api/xbox/register",
            "GET:/api/xbox/check-entitlements/minecraft",
            "GET:/api/xbox/me",
        ),
        BASIC
    )
    ADMIN = (
        "ADMIN",
        "All"
    )

__all__ = [
    "Client",
    "User",
    "Server",
    "Xbox"
]

import uuid
from tortoise import Model, fields

from app.controllers.permissions import ClientPermissions, StandartPermissions


class Client(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    _permissions = fields.TextField()

    def get_permissions(self) -> ClientPermissions:
        return ClientPermissions.deserialize(self._permissions)

    def set_permissions(self, permissions: ClientPermissions) -> None:
        self._permissions = permissions.serialize()

    permissions = property(get_permissions, set_permissions)

    class PydanticMeta:
        exclude = ("_permissions", )
        computed = ("get_permissions", )

    class Meta:
        abstract = True


class User(Client):
    _permissions = fields.TextField(default=StandartPermissions.USER.permissions.serialize())
    username = fields.CharField(64, unique=True)
    password = fields.CharField(128)
    email = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_disabled = fields.BooleanField(default=False)
    is_super = fields.BooleanField(default=False)

    servers: fields.ReverseRelation["Server"]
    xbox_accounts: fields.ReverseRelation["Xbox"]

    class PydanticMeta:
        exclude = ("password", "created_at", "modified_at")

    class Meta:
        table = "user"


class Server(Client):
    _permissions = fields.TextField(default=StandartPermissions.SERVER.permissions.serialize())
    host = fields.CharField(64, unique=True)
    name = fields.CharField(64)
    secret = fields.CharField(128)
    email = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_disabled = fields.BooleanField(default=False)

    owner: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="servers"
    )

    class PydanticMeta:
        exclude = ("secret", "created_at", "modified_at")

    class Meta:
        table = "server"


class Xbox(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_disabled = fields.BooleanField(default=False)

    owner: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="xbox_accounts",
    )

    class Meta:
        table = "xbox"

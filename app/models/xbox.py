__all__ = ["Xbox"]

from uuid import uuid4
from tortoise import Model, fields


class Xbox(Model):
    id = fields.UUIDField(pk=True, default=uuid4())
    owner = fields.ForeignKeyField("models.User", related_name="linked_xbox_accounts")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_disabled = fields.BooleanField(default=False)

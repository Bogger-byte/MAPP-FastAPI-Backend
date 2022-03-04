__all__ = [
    "authorize_server",
    "get_current_server"
]

from fastapi import Depends

from app.controllers.security import verify_password, JWTToken
from app import exceptions as exc
from app import schemas
from app import models

from .jwt import require_jwt_access_token


async def authorize_server(
        user_obj: schemas.User,
        client_id: str,
        client_secret: str
) -> schemas.Server:
    server_obj = await models.Server.get_or_none(id=client_id)
    if server_obj is None:
        raise exc.credentials_exception
    if not verify_password(client_secret, server_obj.api_key):
        raise exc.credentials_exception
    if server_obj.is_disabled:
        raise exc.deleted_exception
    await user_obj.fetch_related("linked_servers")
    if server_obj not in user_obj.__getattribute__("linked_servers"):
        raise exc.forbidden_act_exception
    return await schemas.Server.from_tortoise_orm(server_obj)


async def get_current_server(
        token: JWTToken = Depends(require_jwt_access_token)
) -> schemas.Server:
    if token.is_expired:
        raise exc.credentials_exception
    user_obj = await models.Server.get_or_none(id=token.subject)
    if user_obj is None:
        raise exc.credentials_exception
    if user_obj.is_disabled:
        raise exc.deleted_exception
    return await schemas.Server.from_tortoise_orm(user_obj)

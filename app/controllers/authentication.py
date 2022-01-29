__all__ = ["authenticate_user", "get_current_user", "get_current_admin", "authorize_server"]

from datetime import datetime

from fastapi import Depends, Query, Header
from fastapi.security import OAuth2PasswordBearer

from controllers import exceptions as exc
from controllers.security import verify_password, decode_jwt

import models
import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def authenticate_user(
        username: str,
        password: str
) -> schemas.User:
    user_obj = await models.User.get_or_none(username=username)
    if user_obj is None:
        raise exc.credentials_exception
    if not verify_password(password, user_obj.password):
        raise exc.credentials_exception
    return await schemas.User.from_tortoise_orm(user_obj)


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> schemas.User:
    payload = decode_jwt(token)
    if payload is None:
        raise exc.credentials_exception
    username = payload.get("sub")
    expire = payload.get("exp")
    if username is None or expire is None:
        raise exc.credentials_exception

    if datetime.utcfromtimestamp(expire) < datetime.utcnow():
        raise exc.credentials_exception
    user_obj = await models.User.get_or_none(username=username)
    if user_obj is None:
        raise exc.credentials_exception
    if user_obj.is_disabled:
        raise exc.object_was_deleted
    return await schemas.User.from_tortoise_orm(user_obj)


async def get_current_admin(
        token: str = Depends(oauth2_scheme)
) -> schemas.User:
    user = await get_current_user(token)
    if not user.is_super:
        raise exc.forbidden_act_exception
    return user


async def authorize_server(
        host: str = Query(..., regex=schemas.ip_validation_regex),
        api_key: str = Header(...)
) -> schemas.Server:
    server_obj = await models.Server.get_or_none(host=host)
    if server_obj is None:
        raise exc.credentials_exception
    if not verify_password(api_key, server_obj.api_key):
        raise exc.credentials_exception
    if server_obj.is_disabled:
        raise exc.object_was_deleted
    return await schemas.Server.from_tortoise_orm(server_obj)


# user_obj = await models.User.get_or_none(username=user.username)
# await user_obj.fetch_related("linked_servers")
# linked_server_hosts = [server.host for server in list(user_obj.linked_servers)]
# if host not in linked_server_hosts:
#     raise exc.forbidden_act_exception
#
# server_obj = await models.Server.get_or_none(host=host)
# if server_obj is None:
#     raise exc.not_exist_exception

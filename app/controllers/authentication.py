__all__ = [
    "oauth2_scheme",
    "authorize_user",
    "get_current_user",
    "get_current_admin",
    "authorize_server",
    "get_current_server",
    "require_jwt_token"
]

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import models
import schemas
from controllers import exceptions as exc
from controllers.security import verify_password, JWTToken


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/jwt/token",
    scopes={scope.value: "" for scope in schemas.Scopes}
)


def require_jwt_token(
        token: str = Depends(oauth2_scheme)
) -> JWTToken:
    try:
        return JWTToken(token)
    except ValueError:
        raise exc.validation_exception


async def authorize_user(
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
        token: JWTToken = Depends(require_jwt_token)
) -> schemas.User:
    if token.is_expired:
        raise exc.credentials_exception
    user_obj = await models.User.get_or_none(id=token.subject)
    if user_obj is None:
        raise exc.credentials_exception
    if user_obj.is_disabled:
        raise exc.object_was_deleted
    return await schemas.User.from_tortoise_orm(user_obj)


async def get_current_admin(
        token: JWTToken = Depends(require_jwt_token)
) -> schemas.User:
    user = await get_current_user(token)
    if not user.is_super:
        raise exc.forbidden_act_exception
    return user


async def authorize_server(
        client_id: str,
        client_secret: str
) -> schemas.Server:
    server_obj = await models.Server.get_or_none(id=client_id)
    if server_obj is None:
        raise exc.credentials_exception
    if not verify_password(client_secret, server_obj.api_key):
        raise exc.credentials_exception
    if server_obj.is_disabled:
        raise exc.object_was_deleted
    return await schemas.Server.from_tortoise_orm(server_obj)


async def get_current_server(
        token: JWTToken = Depends(require_jwt_token)
) -> schemas.Server:
    if token.is_expired:
        raise exc.credentials_exception
    user_obj = await models.Server.get_or_none(id=token.subject)
    if user_obj is None:
        raise exc.credentials_exception
    if user_obj.is_disabled:
        raise exc.object_was_deleted
    return await schemas.Server.from_tortoise_orm(user_obj)

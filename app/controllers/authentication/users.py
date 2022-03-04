__all__ = [
    "authorize_user",
    "get_current_user",
    "get_current_admin"
]

from fastapi import Depends

from app.controllers.security import verify_password, JWTToken
from app import exceptions as exc
from app import schemas
from app import models

from .jwt import require_jwt_access_token


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
        token: JWTToken = Depends(require_jwt_access_token)
) -> schemas.User:
    if token.is_expired:
        raise exc.credentials_exception
    user_obj = await models.User.get_or_none(id=token.subject)
    if user_obj is None:
        raise exc.credentials_exception
    if user_obj.is_disabled:
        raise exc.deleted_exception
    return await schemas.User.from_tortoise_orm(user_obj)


async def get_current_admin(
        token: JWTToken = Depends(require_jwt_access_token)
) -> schemas.User:
    user = await get_current_user(token)
    if not user.is_super:
        raise exc.forbidden_act_exception
    return user

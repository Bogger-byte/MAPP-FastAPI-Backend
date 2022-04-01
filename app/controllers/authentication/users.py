__all__ = [
    "authorize_user",
    "get_current_user",
]

from fastapi import Depends, Request, HTTPException, status

from app.controllers.security import verify_password, JWTToken
from app import schemas
from app import models

from .jwt import require_jwt_access_token
from .exceptions import credentials_exception


async def authorize_user(
        username: str,
        password: str
) -> models.User:
    user_obj = await models.User.get_or_none(username=username)
    if user_obj is None:
        raise credentials_exception
    if not verify_password(password, user_obj.password):
        raise credentials_exception
    return user_obj


async def get_current_user(
        request: Request,
        token: JWTToken = Depends(require_jwt_access_token)
) -> schemas.User:
    user_obj = await models.User.get_or_none(id=token.subject)
    if user_obj is None:
        raise credentials_exception
    if user_obj.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was disabled"
        )
    if not user_obj.permissions.is_permitted_to(request.method, request.url.path):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    return await schemas.User.from_tortoise_orm(user_obj)

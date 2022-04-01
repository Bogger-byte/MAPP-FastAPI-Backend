__all__ = [
    "authorize_server",
    "get_current_server"
]

from fastapi import Depends, Request, HTTPException, status

from app.controllers.security import verify_password, JWTToken
from app import schemas
from app import models

from .jwt import require_jwt_access_token
from .exceptions import credentials_exception


async def authorize_server(
        user_obj: models.User,
        client_id: str,
        client_secret: str
) -> schemas.Server:
    server_obj = await models.Server.get_or_none(id=client_id)
    if server_obj is None:
        raise credentials_exception
    if not verify_password(client_secret, server_obj.secret):
        raise credentials_exception
    if server_obj.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server was disabled"
        )
    await user_obj.fetch_related("servers")
    if server_obj not in user_obj.__getattribute__("servers"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    return await schemas.Server.from_tortoise_orm(server_obj)


async def get_current_server(
        request: Request,
        token: JWTToken = Depends(require_jwt_access_token)
) -> schemas.Server:
    server_obj = await models.Server.get_or_none(id=token.subject)
    if server_obj is None:
        raise credentials_exception
    if server_obj.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server was disabled"
        )
    if not server_obj.permissions.is_permitted_to(request.method, request.url.path):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    return await schemas.Server.from_tortoise_orm(server_obj)

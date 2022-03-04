__all__ = [
    "require_jwt_access_token",
    "require_jwt_refresh_token"
]

from fastapi import Depends, Header
from app.controllers.security import JWTToken
from app import exceptions as exc

from . import oauth2_scheme


def require_jwt_access_token(
        access_token: str = Depends(oauth2_scheme)
) -> JWTToken:
    try:
        jwt_token = JWTToken(access_token)
    except ValueError:
        raise exc.validation_exception
    if not jwt_token.is_access_token:
        raise exc.validation_exception
    return jwt_token


def require_jwt_refresh_token(
        refresh_token: str = Header(...)
) -> JWTToken:
    try:
        jwt_token = JWTToken(refresh_token)
    except ValueError:
        raise exc.validation_exception
    if not jwt_token.is_refresh_token:
        raise exc.validation_exception
    return jwt_token

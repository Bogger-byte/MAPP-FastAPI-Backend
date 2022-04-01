__all__ = [
    "require_jwt_access_token",
    "require_jwt_refresh_token"
]

from fastapi import Depends, Header, HTTPException, status
from app.controllers.security import JWTToken

from . import oauth2_scheme


def require_jwt_access_token(
        token: str = Depends(oauth2_scheme)
) -> JWTToken:
    """
    Requires JWT access token for request\n
    :param token: depends on fastapi oauth2_scheme
    :return JWTToken: JWT token object
    :raise HTTPException: if token is not valid or expired
    """
    try:
        jwt_token = JWTToken.decode(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error while decoding JWT token"
        )
    if not jwt_token.is_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provided token is not access token"
        )
    return jwt_token


def require_jwt_refresh_token(
        refresh_token: str = Header(...)
) -> JWTToken:
    """
    Requires JWT refresh token for request\n
    :param refresh_token: jwt token provided in header
    :return JWTToken: JWT token object
    :raise HTTPException: if token is not valid or expired
    """
    try:
        jwt_token = JWTToken.decode(refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error while decoding JWT token"
        )
    if not jwt_token.is_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provided token is not access token"
        )
    return jwt_token

__all__ = []

import logging

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.controllers.authentication import (
    authorize_user,
    authorize_server,
    require_jwt_refresh_token
)
from app.controllers.security import JWTToken
from app.schemas import Scopes, CredentialsValidationForm

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/jwt/token")
async def login_for_access_token(
        credentials: CredentialsValidationForm = Depends(),
) -> JSONResponse:
    """
    Provides access and refresh token for issuers\n
    :param credentials: CredentialsValidationForm
    :return: Refresh and access token
    """
    user_obj = await authorize_user(credentials.username, credentials.password)
    subject = user_obj
    if Scopes.MINECRAFT_SERVER.value in credentials.scopes:
        server_obj = await authorize_server(user_obj, credentials.client_id, credentials.client_secret)
        subject = server_obj

    issuer = type(subject).__name__
    access_token = JWTToken(_type="access", subject=str(subject.id), issuer=issuer)
    refresh_token = JWTToken(_type="refresh", subject=str(subject.id), issuer=issuer)
    return JSONResponse(
        content={
            "access_token": access_token.encode(),
            "refresh_token": refresh_token.encode(),
            "access_token_expire": access_token.expire_delta.total_seconds(),
            "refresh_token_expire": refresh_token.expire_delta.total_seconds()
        },
        status_code=status.HTTP_200_OK
    )


@router.post("/jwt/refresh")
async def refresh_access_token(
        token: JWTToken = Depends(require_jwt_refresh_token)
) -> JSONResponse:
    """
    Provides access and refresh token if previous access token was expired\n
    :param token: jwt refresh token
    :return: Refresh and access token
    """
    access_token = JWTToken(_type="access", subject=token.subject, issuer=token.issuer)
    refresh_token = JWTToken(_type="refresh", subject=token.subject, issuer=token.issuer)
    return JSONResponse(
        content={
            "access_token": access_token.encode(),
            "refresh_token": refresh_token.encode(),
            "access_token_expire": access_token.expire_delta.total_seconds(),
            "refresh_token_expire": refresh_token.expire_delta.total_seconds()
        },
        status_code=status.HTTP_200_OK
    )

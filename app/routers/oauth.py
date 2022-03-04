__all__ = []

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.controllers.authentication import (
    authorize_user,
    authorize_server,
    require_jwt_refresh_token
)
from app.controllers.security import JWTToken
from app.schemas import Scopes, CredentialsValidationForm
from app.settings import (
    JWT_ACCESS_TOKEN_EXPIRE,
    JWT_REFRESH_TOKEN_EXPIRE,
)

router = APIRouter()


@router.post("/jwt/token")
async def login_for_access_token(
        credentials: CredentialsValidationForm = Depends(),
) -> JSONResponse:
    """
    Provides access and refresh token for issuers
    :param credentials: CredentialsValidationForm
    :return: Refresh and access token
    """
    user_obj = await authorize_user(credentials.username, credentials.password)
    subject = user_obj
    if Scopes.MINECRAFT_SERVER.value in credentials.scopes:
        server_obj = await authorize_server(user_obj, credentials.client_id, credentials.client_secret)
        subject = server_obj

    access_token = JWTToken.create_access_token(subject=str(subject.id))
    refresh_token = JWTToken.create_refresh_token(subject=str(subject.id))
    return JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expire": JWT_ACCESS_TOKEN_EXPIRE.total_seconds(),
            "refresh_token_expire": JWT_REFRESH_TOKEN_EXPIRE.total_seconds()
        },
        status_code=status.HTTP_200_OK
    )


@router.post("/jwt/refresh")
async def refresh_access_token(
        token: JWTToken = Depends(require_jwt_refresh_token)
) -> JSONResponse:
    """
    Provides access and refresh token if previous access token was expired
    :param token: jwt refresh token
    :return: Refresh and access token
    """
    access_token = JWTToken.create_access_token(subject=token.subject)
    refresh_token = JWTToken.create_refresh_token(subject=token.subject)
    return JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expire": JWT_ACCESS_TOKEN_EXPIRE.total_seconds(),
            "refresh_token_expire": JWT_REFRESH_TOKEN_EXPIRE.total_seconds()
        },
        status_code=status.HTTP_200_OK
    )

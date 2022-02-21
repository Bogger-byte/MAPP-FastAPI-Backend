__all__ = []

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from controllers import exceptions as exc
from controllers.authentication import authorize_user, authorize_server, require_jwt_token
from controllers.security import JWTToken
from schemas import Scopes, CredentialsValidationForm

router = APIRouter()


@router.post("/jwt/token")
async def login_for_access_token(
        credentials: CredentialsValidationForm = Depends(),
) -> JSONResponse:

    subject = await authorize_user(credentials.username, credentials.password)
    if Scopes.MINECRAFT_SERVER.value in credentials.scopes:
        subject = await authorize_server(credentials.client_id, credentials.client_secret)

    access_token = JWTToken.create_access_token(subject=str(subject.id))
    refresh_token = JWTToken.create_refresh_token(subject=str(subject.id))
    return JSONResponse(
        content={"access_token": access_token, "refresh_token": refresh_token},
        status_code=status.HTTP_200_OK
    )


@router.post("/jwt/refresh")
async def refresh_access_token(
        token: JWTToken = Depends(require_jwt_token)
) -> JSONResponse:
    if not token.is_refresh_token:
        raise exc.validation_exception

    access_token = JWTToken.create_access_token(subject=token.subject)
    refresh_token = JWTToken.create_refresh_token(subject=token.subject)
    return JSONResponse(
        content={"access_token": access_token, "refresh_token": refresh_token},
        status_code=status.HTTP_200_OK
    )

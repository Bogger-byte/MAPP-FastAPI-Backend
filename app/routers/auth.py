__all__ = []

from fastapi import APIRouter, Depends
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from datetime import timedelta

from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from controllers.authentication import authorize_user
from controllers.security import encode_jwt


router = APIRouter()


@router.post("/token")
async def login_for_access_token(
        credentials: OAuth2PasswordRequestForm = Depends()
) -> JSONResponse:
    user = await authorize_user(credentials.username, credentials.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = encode_jwt(data={"sub": user.username}, expires_delta=access_token_expires)
    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=status.HTTP_200_OK
    )


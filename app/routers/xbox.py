__all__ = []

import logging

from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse

from app import exceptions as exc
from app import models
from app import schemas
from app.controllers import microsoft_oauth as ms_oauth
from app.controllers import minecraft_api as mc_api
from app.controllers.authentication import get_current_user, require_xbox_account

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/register")
async def authorize_with_xbox_account(
        current_user: schemas.User = Depends(get_current_user)
) -> str:
    # return RedirectResponse(url=ms_oauth.generate_oauth_url(state=current_user.id))
    return ms_oauth.generate_oauth_url(state=current_user.id)


@router.get("/token-endpoint")
async def get_xbox_oauth_token(
        response: ms_oauth.MSAuthResponse = Depends()
) -> RedirectResponse:
    if response.have_errors:
        raise exc.validation_exception
    user_obj = await models.User.get_or_none(id=response.state)
    if user_obj is None:
        raise exc.validation_exception

    ms_refresh_token, ms_access_token = await ms_oauth.get_authorization_token(response.code)
    xbox_obj, _ = await models.Xbox.update_or_create(owner=user_obj)
    return RedirectResponse(
        url=f"http://localhost:8080/xbox/check-entitlements/minecraft"
            f"?ms_access_token={ms_access_token}",
    )


@router.get("/check-entitlements/minecraft")
async def check_minecraft_entitlements(
        ms_access_token: str = Query(...)
) -> str:
    mc_access_token = await mc_api.get_authorization_token(ms_access_token)
    user_store = await mc_api.get_store_entitlements(mc_access_token)
    return f"Minecraft owning entitlements = {bool(user_store.items)}"


@router.get("/me")
async def get_my_xbox(
        xbox_account: schemas.Xbox = Depends(require_xbox_account)
) -> schemas.Xbox:
    return xbox_account

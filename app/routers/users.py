__all__ = []

from fastapi import APIRouter, Depends
from starlette import status
from fastapi.responses import JSONResponse
from tortoise.exceptions import IntegrityError

import models
import schemas
import controllers.exceptions as exc
from controllers.authentication import get_current_user, get_current_admin
from controllers.security import get_password_hash


router = APIRouter()


@router.post("/register")
async def create_user(user: schemas.UserCreate):
    try:
        user.password = get_password_hash(user.password)
        user_obj = await models.User.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise exc.already_exist_exception
    return await schemas.User.from_tortoise_orm(user_obj)


@router.get("/me")
async def get_my_user(
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    return current_user


@router.patch("/me")
async def update_my_user(
        updates: schemas.UserUpdate, current_user: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    user_obj = await models.User.get_or_none(id=current_user.id)
    if user_obj is None:
        raise exc.not_exist_exception
    await user_obj.update_from_dict(updates.dict(exclude_none=True))
    await user_obj.save()
    return JSONResponse(
        content=f"{user_obj.id} successfully updated",
        status_code=status.HTTP_200_OK
    )


@router.delete("/me")
async def delete_my_user(
        current_user: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    user_obj = await models.User.get_or_none(id=current_user.id)
    if user_obj is None:
        raise exc.not_exist_exception
    await user_obj.delete()
    return JSONResponse(
        content=f"{user_obj.id} successfully deleted",
        status_code=status.HTTP_200_OK
    )


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: str,
        current_admin: schemas.User = Depends(get_current_admin)
) -> schemas.User:
    user_obj = await models.User.get_or_none(id=user_id)
    if user_obj is None:
        raise exc.not_exist_exception
    return await schemas.User.from_tortoise_orm(user_obj)


@router.patch("/{user_id}")
async def update_user_by_id(
        user_id: str, updates: schemas.UserUpdate,
        current_user: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    user_obj = await models.User.get_or_none(id=user_id)
    if user_obj is None:
        raise exc.not_exist_exception
    await user_obj.update_from_dict(updates.dict(exclude_none=True))
    await user_obj.save()
    return JSONResponse(
        content=f"{user_obj.id} successfully updated",
        status_code=status.HTTP_200_OK
    )


@router.delete("/{user_id}")
async def delete_user_by_id(
        user_id: str,
        current_admin: schemas.User = Depends(get_current_admin)
) -> JSONResponse:
    user_obj = await models.User.get(id=user_id)
    if user_obj is None:
        raise exc.not_exist_exception
    await user_obj.delete()
    return JSONResponse(
        content=f"{user_obj.id} successfully updated",
        status_code=status.HTTP_200_OK
    )

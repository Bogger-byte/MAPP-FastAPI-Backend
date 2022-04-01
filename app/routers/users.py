__all__ = []

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from tortoise.exceptions import IntegrityError

from app import models
from app import schemas
from app.controllers.authentication import get_current_user
from app.controllers.security import get_password_hash

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/register")
async def create_user(
        user: schemas.UserCreate
) -> schemas.User:
    try:
        user.password = get_password_hash(user.password)
        user_obj = await models.User.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with {user.username=} already exist"
        )
    return await schemas.User.from_tortoise_orm(user_obj)


@router.get("/me")
async def get_my_user(
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    return current_user


@router.patch("/me")
async def update_my_user(
        user_update: schemas.UserUpdate,
        current_user: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    user_obj = await models.User.get_or_none(id=current_user.id)
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {current_user.id=} was not found"
        )
    await user_obj.update_from_dict(user_update.dict(exclude_none=True))
    await user_obj.save()
    return JSONResponse(
        content=f"Successfully updated user with {user_obj.id=}",
        status_code=status.HTTP_200_OK
    )


@router.delete("/me")
async def delete_my_user(
        current_user: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    user_obj = await models.User.get_or_none(id=current_user.id)
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {current_user.id=} was not found"
        )
    await user_obj.delete()
    return JSONResponse(
        content=f"Successfully deleted user with {user_obj.id=}",
        status_code=status.HTTP_200_OK
    )


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: str
) -> schemas.User:
    user_obj = await models.User.get_or_none(id=user_id)
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id=} was not found"
        )
    return await schemas.User.from_tortoise_orm(user_obj)


@router.patch("/{user_id}")
async def update_user_by_id(
        user_id: str, updates: schemas.UserUpdate,
        current_user: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    user_obj = await models.User.get_or_none(id=user_id)
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id=} was not found"
        )
    await user_obj.update_from_dict(updates.dict(exclude_none=True))
    await user_obj.save()
    return JSONResponse(
        content=f"Successfully updated user with {user_obj.id=}",
        status_code=status.HTTP_200_OK
    )


@router.delete("/{user_id}")
async def delete_user_by_id(
        user_id: str,
        current_admin: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    user_obj = await models.User.get(id=user_id)
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id=} was not found"
        )
    await user_obj.delete()
    return JSONResponse(
        content=f"Successfully deleted user with {user_obj.id=}",
        status_code=status.HTTP_200_OK
    )

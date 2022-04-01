__all__ = []

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from tortoise.exceptions import IntegrityError

from app import models
from app import schemas
from app.controllers import servers_folder
from app.controllers.authentication import (
    get_current_user,
    get_current_server
)
from app.controllers.security import get_password_hash


router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/register")
async def create_server(
        server: schemas.ServerCreate,
        user: schemas.User = Depends(get_current_user)
) -> schemas.Server:
    try:
        server.secret = get_password_hash(server.secret)
        user_obj = await models.User.get_or_none(username=user.username)
        server_obj = await models.Server.create(**server.dict(exclude_unset=True), owner=user_obj)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Server with {server.host=} already exist"
        )
    servers_folder.create_new(server_obj.id)
    return await schemas.Server.from_tortoise_orm(server_obj)


@router.get("/me")
async def get_my_server(
        current_server: schemas.Server = Depends(get_current_server)
) -> schemas.Server:
    return current_server


@router.patch("/me")
async def update_my_server(
        server_update: schemas.ServerUpdate,
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    server_obj = await models.Server.get_or_none(id=current_server.id)
    if server_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with {current_server.id=} was not found"
        )
    await server_obj.update_from_dict(server_update.dict(exclude_none=True))
    await server_obj.save()
    return JSONResponse(
        content=f"Successfully updated server with {server_obj.id=}",
        status_code=status.HTTP_200_OK
    )


@router.delete("/me")
async def delete_my_server(
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    server_obj = await models.Server.get(id=current_server.id)
    if server_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with {current_server.id=} was not found"
        )
    server_obj.is_disabled = True
    await server_obj.save()
    return JSONResponse(
        content=f"Successfully deleted server with {server_obj.id=}",
        status_code=status.HTTP_200_OK
    )


@router.get("/{server_id}")
async def get_server_by_id(
        server_id: str,
) -> schemas.Server:
    server_obj = await models.Server.get_or_none(id=server_id)
    if server_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with {server_id=} was not found"
        )
    return await schemas.Server.from_tortoise_orm(server_obj)


@router.patch("/{server_id}")
async def update_server_by_id(
        server_id: str,
        updates: schemas.ServerUpdate,
        current_admin: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    server_obj = await models.Server.get_or_none(id=server_id)
    if server_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with {server_id=} was not found"
        )
    await server_obj.update_from_dict(updates.dict(exclude_none=True))
    await server_obj.save()
    return JSONResponse(
        content=f"Successfully updated server with {server_obj.id=}",
        status_code=status.HTTP_200_OK
    )


@router.delete("/{server_id}")
async def delete_server_by_id(
        server_id: str,
        current_admin: schemas.User = Depends(get_current_user)
) -> JSONResponse:
    server_obj = await models.Server.get_or_none(id=server_id)
    if server_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with {server_id=} was not found"
        )
    await server_obj.delete()
    server_obj.is_disabled = True
    await server_obj.save()
    return JSONResponse(
        content=f"Successfully deleted server with {server_obj.id=}",
        status_code=status.HTTP_200_OK
    )


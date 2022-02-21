__all__ = []

from fastapi import APIRouter, Depends
from starlette import status
from fastapi.responses import JSONResponse

from tortoise.exceptions import IntegrityError

from controllers.authentication import get_current_user, get_current_server, get_current_admin
from controllers.security import get_password_hash
from controllers import exceptions as exc
from controllers import servers_folder

import schemas
import models

router = APIRouter()


@router.post("/register")
async def create_server(
        server: schemas.ServerCreate,
        user: schemas.User = Depends(get_current_user)
) -> schemas.Server:
    try:
        server.api_key = get_password_hash(server.api_key)
        user_obj = await models.User.get(username=user.username)
        server_obj = await models.Server.create(**server.dict(exclude_unset=True), owner=user_obj)
    except IntegrityError:
        raise exc.already_exist_exception
    servers_folder.create_new(server_obj.id)
    return await schemas.Server.from_tortoise_orm(server_obj)


@router.get("/me")
async def get_my_server(
        current_server: schemas.Server = Depends(get_current_server)
) -> schemas.Server:
    return current_server


@router.patch("/me")
async def update_my_server(
        updates: schemas.ServerUpdate,
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    server_obj = await models.Server.get_or_none(id=current_server.id)
    if server_obj is None:
        raise exc.not_exist_exception
    await server_obj.update_from_dict(updates.dict(exclude_none=True))
    await server_obj.save()
    return JSONResponse(
        content=f"{server_obj.id} successfully updated",
        status_code=status.HTTP_200_OK
    )


@router.delete("/me")
async def delete_my_server(
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    server_obj = await models.Server.get(id=current_server.id)
    if server_obj is None:
        raise exc.not_exist_exception
    server_obj.is_disabled = True
    await server_obj.save()
    return JSONResponse(
        content=f"{server_obj.id} successfully deleted",
        status_code=status.HTTP_200_OK
    )


@router.get("/{server_id}")
async def get_server_by_id(
        server_id: str,
        current_admin: schemas.User = Depends(get_current_admin)
) -> schemas.Server:
    server_obj = await models.Server.get_or_none(id=server_id)
    if server_obj is None:
        raise exc.not_exist_exception
    return await schemas.Server.from_tortoise_orm(server_obj)


@router.patch("/{server_id}")
async def update_server_by_id(
        server_id: str,
        updates: schemas.ServerUpdate,
        current_admin: schemas.User = Depends(get_current_admin)
) -> JSONResponse:
    server_obj = await models.Server.get_or_none(id=server_id)
    if server_obj is None:
        raise exc.not_exist_exception
    await server_obj.update_from_dict(updates.dict(exclude_none=True))
    await server_obj.save()
    return JSONResponse(
        content=f"{server_obj.id} successfully updated",
        status_code=status.HTTP_200_OK
    )


@router.delete("/{server_id}")
async def delete_server_by_id(
        server_id: str,
        current_admin: schemas.User = Depends(get_current_admin)
) -> JSONResponse:
    server_obj = await models.Server.get_or_none(id=server_id)
    if server_obj is None:
        raise exc.not_exist_exception
    await server_obj.delete()
    server_obj.is_disabled = True
    await server_obj.save()
    return JSONResponse(
        content=f"{server_obj.id} successfully deleted",
        status_code=status.HTTP_200_OK
    )

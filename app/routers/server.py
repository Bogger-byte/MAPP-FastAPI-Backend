__all__ = []

import os.path

from fastapi import APIRouter, Depends, Body, File, Query, UploadFile
from starlette import status
from fastapi.responses import JSONResponse, FileResponse

import models
import schemas

from controllers.authentication import get_current_server
from controllers import exceptions as exc
from controllers import servers_folder


router = APIRouter()


@router.get("/{host}/info")
async def get_server_info(
        host: str = Query(..., regex=schemas.ip_validation_regex)
) -> NotImplementedError:
    pass


@router.post("/{host}/players-data")
async def upload_players_data(
        players_data: schemas.PlayersData = Body(...),
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    await models.ServerData(
        id=current_server.id,
        players_data=players_data.json(),
        online=True
    ).save()
    return JSONResponse(
        content="Data accepted",
        status_code=status.HTTP_202_ACCEPTED
    )


@router.get("/{host}/players-data")
async def get_players_data(
        host: str = Query(..., regex=schemas.ip_validation_regex)
) -> JSONResponse:
    server_obj = await models.Server.get_or_none(host=host)
    if server_obj is None:
        raise exc.not_exist_exception
    server_data_obj = await models.ServerData.get(server_obj.id)
    return JSONResponse(
        content=server_data_obj.players_data,
        status_code=status.HTTP_200_OK
    )


@router.post("/{host}/region-image")
async def upload_region_images(
        regions: list[UploadFile] = File(...),
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    server_regions_folder = servers_folder.get_regions_path(current_server.id)
    # bg_tasks.add_task(servers_folder.regions.process_mca_files, regions)
    return JSONResponse(
        content=f"Path: {server_regions_folder}/",
        status_code=status.HTTP_200_OK
    )


@router.get("/{host}/region-image")
async def get_region_image(
        world: str,
        region_x: int,
        region_z: int,
        host: str = Query(..., regex=schemas.ip_validation_regex)
) -> FileResponse:
    server_obj = await models.Server.get_or_none(host=host)
    if server_obj is None:
        raise exc.not_exist_exception
    file_path = f"servers/regions/{server_obj.id}/{world}_r.{region_x}.{region_z}.mca.png"
    if not os.path.exists(file_path):
        raise exc.not_exist_exception
    return FileResponse(file_path)

__all__ = []

from os import path

from fastapi import APIRouter, Depends, Body, File, Query, UploadFile, status
from fastapi.responses import JSONResponse, FileResponse

from app.controllers.authentication import get_current_server
from app.controllers import servers_folder
from app import exceptions as exc

from app import schemas
from app import models


router = APIRouter()


@router.get("/{host}/info")
async def get_server_info(
        host: str = Query(..., regex=schemas.ip_validation_regex)
) -> NotImplementedError:
    """
    Provides basic info about Minecraft server for any issuers
    :param host: server host
    :return: Basic info about Minecraft server
    """
    pass


@router.post("/{host}/players-data")
async def upload_players_data(
        players_data: schemas.PlayersData = Body(...),
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    """
    Provides uploading players data
    :param players_data: List of player coordinates
    :param current_server: Authorization header
    :return: 200
    """
    print(f"Server {current_server.id} sent players data: {players_data.dict()}")
    # await models.ServerData(
    #     id=current_server.id,
    #     players_data=players_data.json(),
    #     online=True
    # ).save()
    return JSONResponse(
        content="Data accepted",
        status_code=status.HTTP_202_ACCEPTED
    )


@router.get("/{host}/players-data")
async def get_players_data(
        host: str = Query(..., regex=schemas.ip_validation_regex)
) -> JSONResponse:
    """
    Provides list of player coordinates for any issuers
    :param host: Minecraft server host
    :return: List of player coordinates
    """
    # server_obj = await models.Server.get_or_none(host=host)
    # if server_obj is None:
    #     raise exc.not_exist_exception
    # server_data_obj = await models.ServerData.is_expired(server_obj.id)
    # return JSONResponse(
    #     content=server_data_obj.players_data,
    #     status_code=status.HTTP_200_OK
    # )
    pass


@router.post("/{host}/region-image")
async def upload_region_images(
        regions: list[UploadFile] = File(...),
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    """
    Provides uploading PNG region tiles
    :param regions: List of PNG files
    :param current_server: Authorization header
    :return: Save path
    """
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
    """
    Provides PNG image of region tile for any issuers
    :param world: Minecraft world name
    :param region_x: Minecraft region x cord
    :param region_z: Minecraft region y cord
    :param host: Minecraft server host
    :return: PNG image of region tile
    """
    server_obj = await models.Server.get_or_none(host=host)
    if server_obj is None:
        raise exc.not_exist_exception
    file_path = f"servers/regions/{server_obj.id}/{world}_r.{region_x}.{region_z}.mca.png"
    if not path.exists(file_path):
        raise exc.not_exist_exception
    return FileResponse(file_path)

__all__ = []

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Body, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse

from app.controllers.authentication import get_current_server
from app.controllers.broadcasts import broadcast
from app.controllers import servers_folder
from app import schemas
from app import models


router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/me/info")
async def publish_my_info(
        info: schemas.ServerInfo = Body(...),
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    """
    Provides uploading server info
    """
    channel = "servers_info"
    message = {
        "is_enabled": info.is_enabled,
        "id": str(current_server.id),
        "name": current_server.name,
        "host": current_server.host,
        "players_online": info.players_online
    }
    await broadcast.add_to_queue(channel=channel, message=message)
    channel = f"server_data:{current_server.id}"
    await broadcast.publish(channel=channel, message={"server_info": message})
    return JSONResponse(
        content="Successfully uploaded",
        status_code=status.HTTP_200_OK
    )


@router.post("/me/players-data")
async def publish_players_data(
        players_data: schemas.PlayersData = Body(...),
        current_server: schemas.Server = Depends(get_current_server)
) -> JSONResponse:
    """
    Provides uploading players data
    """
    channel = f"server_data:{current_server.id}"
    await broadcast.publish(channel=channel, message=players_data.dict())
    return JSONResponse(
        content="Successfully uploaded",
        status_code=status.HTTP_200_OK
    )


@router.post("/me/regions")
async def publish_region_images(
        region_image_uploads: list[UploadFile] = File(...),
        current_server: schemas.Server = Depends(get_current_server),
) -> JSONResponse:
    """
    Provides uploading MCA region tiles
    """
    servers_folder.save_to_folder(current_server.id, region_image_uploads)

    channel = f"server_data:{current_server.id}"
    message = {"updated_regions": [upload.filename for upload in region_image_uploads]}
    await broadcast.publish(channel=channel, message=message)

    logger.info([upload.filename for upload in region_image_uploads])
    return JSONResponse(
        content=f"Successfully uploaded",
        status_code=status.HTTP_200_OK
    )


@router.get("/{server_id}/regions")
async def get_available_regions(
        server_id: str
) -> JSONResponse:
    """
    Provides list of all available regions for this server
    """
    server_obj = await models.Server.get_or_none(id=server_id)
    if server_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with {server_id=} was not found"
        )
    all_regions = servers_folder.get_all("regions", server_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"regions": all_regions}
    )


@router.get("/{server_id}/regions/{world}/{region_x}/{region_z}")
async def get_region_image(
        world: str,
        region_x: int,
        region_z: int,
        server_id: str
) -> FileResponse:
    """
    Provides PNG image of region tile for any issuers
    """
    server_obj = await models.Server.get_or_none(id=server_id)
    if server_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with {server_id=} was not found"
        )
    regions_folder = servers_folder.get_folder("regions", server_obj.id)
    path = Path(f"{regions_folder}/{world}_r.{region_x}.{region_z}.png")
    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with {path=} was not found"
        )
    return FileResponse(path)

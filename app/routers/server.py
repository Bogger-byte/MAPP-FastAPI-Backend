__all__ = []

import os.path

from fastapi import APIRouter, Query, Depends, Body, File
from starlette import status
from fastapi.responses import JSONResponse, FileResponse

import models
import schemas

from controllers.authentication import authorize_server
from controllers import exceptions as exc
from controllers import server_snapshot


router = APIRouter()


@router.get("/info")
async def get_server_info(
        host: str = Query(..., regex=schemas.ip_validation_regex)
) -> NotImplementedError:
    pass


@router.get("/regions")
async def get_region_image(
        world: str,
        region_x: int,
        region_y: int,
        host: str = Query(..., regex=schemas.ip_validation_regex),
) -> FileResponse:
    server_obj = await models.Server.get_or_none(host=host)
    if server_obj is None:
        raise exc.not_exist_exception
    file_path = f"servers/regions/{server_obj.id}/{world}_r.{region_x}.{region_y}.png"
    if not os.path.exists(file_path):
        raise exc.not_exist_exception
    return FileResponse(file_path)


@router.post("/players-data")
async def upload_players_data(
        players_data: schemas.PlayersData = Body(...),
        current_server: schemas.Server = Depends(authorize_server)
) -> JSONResponse:
    return JSONResponse(
        content="Data accepted",
        status_code=status.HTTP_202_ACCEPTED
    )


@router.post("/upload-region-image")
async def upload_region_image(
        world: str,
        region_x: int,
        region_y: int,
        image: schemas.UploadPngFile = File(...),
        current_server: schemas.Server = Depends(authorize_server)
) -> JSONResponse:
    file_path = f"servers/regions/{current_server.id}/{world}_r.{region_x}.{region_y}.png"
    server_snapshot.save_image_file(file_path, image)
    return JSONResponse(
        content=file_path,
        status_code=status.HTTP_202_ACCEPTED
    )

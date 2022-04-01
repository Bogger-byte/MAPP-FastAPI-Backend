__all__ = [
    "create_new",
    "get_folder"
]

import logging
import os
import shutil
from pathlib import Path
from typing import Optional

from fastapi import UploadFile

from app.settings import SERVERS_FILES_FOLDER

logger = logging.getLogger(f"app.{__name__}")


def create_new(server_uuid: str) -> None:
    os.makedirs(f"{SERVERS_FILES_FOLDER}/regions/{server_uuid}")
    os.makedirs(f"{SERVERS_FILES_FOLDER}/cache/{server_uuid}")
    os.makedirs(f"{SERVERS_FILES_FOLDER}/logs/{server_uuid}")


def get_folder(
        _type: str,
        server_uuid: str
) -> Optional[Path]:
    str_path = f"{SERVERS_FILES_FOLDER}/{_type}/{server_uuid}"
    path = Path(str_path)
    return path if path.exists() else None


def get_all(
        _type: str,
        server_uuid: str
) -> list[str]:
    folder = get_folder(_type, server_uuid)
    return [abs_path for abs_path in os.listdir(folder)]


def save_to_folder(
        server_uuid: str,
        uploads: list[UploadFile]
) -> None:
    regions_folder = get_folder("regions", server_uuid)
    if regions_folder is None:
        logger.warning(f"Server with id={server_uuid} hasn't initialized folders, perhaps it was deleted?")
    for upload in uploads:
        try:
            file_path = f"{regions_folder}/{upload.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload.file, buffer)
        finally:
            upload.file.close()

__all__ = ["prepare_dirs", "save_image_file"]

import os
import shutil

from fastapi import UploadFile


def prepare_dirs(server_uuid: str) -> None:
    os.makedirs(f"servers/regions/{server_uuid}")
    os.makedirs(f"servers/cache/{server_uuid}")
    os.makedirs(f"servers/logs/{server_uuid}")


def save_image_file(
        file_path: str,
        image: UploadFile
) -> None:
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    finally:
        image.file.close()

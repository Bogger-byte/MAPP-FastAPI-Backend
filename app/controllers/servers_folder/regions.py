__all__ = ["process_mca_files"]

import os
import shutil

import schemas


def process_mca_files(
        server_regions_folder: str,
        region_images: list[schemas.UploadMcaFile]
) -> None:

    pass


def save_image_files(
        server_regions_folder: str,
        region_images: list[schemas.UploadMcaFile],
) -> None:
    for image in region_images:
        try:
            file_path = f"{server_regions_folder}/{image.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        finally:
            image.file.close()

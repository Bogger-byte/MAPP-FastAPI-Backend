__all__ = ["regions", "create_new", "get_regions_path"]

import os
from pathlib import Path
from typing import Union

from app.settings import SERVER_REGIONS, SERVER_CACHE, SERVER_LOGS

from . import regions


def create_new(server_uuid: str) -> None:
    os.makedirs(f"{SERVER_REGIONS}/{server_uuid}")
    os.makedirs(f"{SERVER_CACHE}/{server_uuid}")
    os.makedirs(f"{SERVER_LOGS}/{server_uuid}")


def get_regions_path(
        server_uuid: str
) -> Union[Path, None]:
    folder_path = f"{SERVER_REGIONS}/{server_uuid}"
    return folder_path if os.path.exists(folder_path) else None

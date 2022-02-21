__all__ = ["UploadMcaFile"]

import os
from typing import Type, Any, Iterable, Callable

from starlette.datastructures import UploadFile as StarletteUploadFile


class UploadMcaFile(StarletteUploadFile):
    @classmethod
    def __get_validators__(cls: Type["UploadMcaFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadMcaFile"], v: Any) -> Any:
        if not isinstance(v, StarletteUploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(v)}")
        _, extension = os.path.splitext(v.filename.lower())
        if extension != ".mca":
            raise ValueError(f"Expected .mca file extension, recieved: {extension}")
        return v

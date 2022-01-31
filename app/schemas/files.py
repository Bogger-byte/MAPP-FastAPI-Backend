__all__ = ["UploadPngFile"]

import os
from typing import Type, Any, Iterable, Callable

from fastapi import UploadFile


class UploadPngFile(UploadFile):
    @classmethod
    def __get_validators__(cls: Type["UploadPngFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadPngFile"], v: Any) -> Any:
        if not isinstance(v, UploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(v)}")
        # if v.content_type != "image/png":
        #     raise ValueError("Expected png content type")
        # _, extension = os.path.splitext(v.filename.lower())
        # if extension != ".png":
        #     raise ValueError("Expected png extension")
        return v

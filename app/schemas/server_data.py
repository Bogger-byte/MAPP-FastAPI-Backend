__all__ = ["PlayersData", "PlayerData", "Coordinates"]

from typing import Optional

from pydantic import BaseModel


class Coordinates(BaseModel):
    x: int
    y: Optional[int]
    z: int


class PlayerData(BaseModel):
    uuid: str
    is_force_visible: bool
    name: str
    coordinates: Coordinates


class PlayersData(BaseModel):
    players_data: list[PlayerData]

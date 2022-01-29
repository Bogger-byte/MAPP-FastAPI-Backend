__all__ = ["PlayersData", "PlayerData", "Coordinates"]

from pydantic import BaseModel


class Coordinates(BaseModel):
    x: int
    y: int
    z: int


class PlayerData(BaseModel):
    uuid: str
    is_force_visible: bool
    nickname: str
    coordinates: Coordinates


class PlayersData(BaseModel):
    players_data: list[PlayerData]
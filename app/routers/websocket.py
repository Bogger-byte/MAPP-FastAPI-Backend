__all__ = []

import json
import logging
from typing import Optional, Type

from fastapi import APIRouter, WebSocket
from pydantic import BaseModel, ValidationError, validator
from tortoise.exceptions import DoesNotExist

from app import models
from app.controllers.broadcasts import broadcast
from app.controllers.permissions import StandartPermissions
from app.controllers.security import JWTToken

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


STANDARD_CHANNEL_NAMES = [
    "servers_info",
    "server_data"
]


class Channel(BaseModel):
    name: str
    id: Optional[str] = None

    @validator("name")
    def validate_name(cls: Type["Channel"], v: str) -> str:
        if v not in STANDARD_CHANNEL_NAMES:
            raise ValueError(f"Not a standard channel: {v} -> {STANDARD_CHANNEL_NAMES}")
        return v


class AuthorizationMessage(BaseModel):
    access_token: Optional[str] = None
    channel: Channel


class Object(object):
    pass


@router.websocket("/endpoint")
async def websocket_endpoint(
        websocket: WebSocket
) -> None:
    await websocket.accept()
    try:
        # authentication
        json_message = await websocket.receive_json()
        auth_message = AuthorizationMessage(**json_message)
        token = JWTToken.decode(auth_message.access_token) if auth_message.access_token else None
        client_obj = Object()
        if token and token.issuer == "User":
            client_obj = await models.User.get(id=token.subject)
        elif token and token.issuer == "Server":
            client_obj = await models.Server.get(id=token.subject)
        else:
            client_obj.permissions = StandartPermissions.BASIC.permissions
        channel = auth_message.channel
        if not client_obj.permissions.is_permitted_to("WS", channel.name):
            await websocket.send_json({"error": f"Permission denied for {channel=}"})
            raise ValueError
        # subscription
        scoped_channel = channel.name if channel.id is None else f"{channel.name}:{channel.id}"
        async with broadcast.subscribe(channel=scoped_channel) as subscriber:
            logger.info(f"Client subscribed to {channel=}")
            async for event in subscriber:
                message = json.loads(event.message)
                await websocket.send_json({"channel": event.channel, "message": message})
    except ValidationError:
        await websocket.send_json({"error": f"Invalid auth message"})
    except ValueError or DoesNotExist:
        await websocket.send_json({"error": "Invalid JWT token"})
    finally:
        if websocket.client_state.name != "DISCONNECTED":
            await websocket.close()

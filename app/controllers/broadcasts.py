__all__ = [
    "broadcast"
]

import json
import logging

from broadcaster import Broadcast

logger = logging.getLogger(f"app.{__name__}")


class RedisBroadcast(Broadcast):
    def __init__(self, host: str, port: int):
        url = f"redis://{host}:{port}"
        super().__init__(url)

        self._channels_queue: dict[str, list] = {}

    async def create_channel(self, channel: str) -> None:
        await super().publish(channel, "init")

    async def publish(self, channel: str, message: dict) -> None:
        message = json.dumps(message)
        await super().publish(channel, message)

    async def add_to_queue(self, channel: str, message: dict) -> None:
        if self._channels_queue.get(channel) is None:
            self._channels_queue[channel] = []
        self._channels_queue[channel].append(message)

    async def publish_queue(self) -> None:
        for channel, queue in self._channels_queue.items():
            message = {"queue": queue}
            await self.publish(channel, message)

        self._channels_queue.clear()


broadcast = RedisBroadcast(host="localhost", port=6379)

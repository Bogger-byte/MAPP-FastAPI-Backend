__all__ = ["ServerData"]

from redis import Redis
from rom import Model, columns


class ServerData(Model):
    __conn = Redis(host="localhost", port=6379, db=1)

    id = columns.PrimaryKey()
    players_data = columns.Json(required=True)
    online = columns.Boolean(required=True)

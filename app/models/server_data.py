__all__ = ["ServerData"]


from rom import util, Model, columns

util.set_connection_settings(host="localhost", db=1)


class ServerData(Model):
    id = columns.PrimaryKey()
    players_data = columns.Json(required=True)

from tortoise import Tortoise


Tortoise.init_models(["app.models"], "models")


from .user import *
from .server import *
from .server_data import *
from .auth import *
from .xbox import *

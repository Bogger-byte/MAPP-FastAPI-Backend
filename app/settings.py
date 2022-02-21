from datetime import timedelta

DATABASE_URL = "sqlite://./database/user.db"

MODELS_FILE = "models"

SERVER_REGIONS = "servers/regions"
SERVER_CACHE = "servers/cache"
SERVER_LOGS = "servers/logs"

JWT_SECRET = "SECRET"
JWT_DECODE_ALGORYTHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRE = timedelta(days=15)

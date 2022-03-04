from datetime import timedelta

DATABASE_URL = "sqlite://app/.database/user.db"

MODELS_FILE = "app.models"

SERVER_REGIONS = ".servers/regions"
SERVER_CACHE = ".servers/cache"
SERVER_LOGS = ".servers/logs"

JWT_SECRET = "SECRET"
JWT_DECODE_ALGORYTHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRE = timedelta(days=1)

AZURE_CLIENT_ID = "83987e01-fa4c-4107-9290-7479a1361d6b"
AZURE_CLIENT_SECRET = "ngZ7Q~1q2s~spkq.AqbYg9L9fCFZ4WUlo_qRs"
AZURE_REDIRECT_URI = "http://localhost:8080/xbox/token-endpoint"

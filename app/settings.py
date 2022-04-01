from datetime import timedelta

DATABASE_URL = "sqlite://app/.database/user.db"

MODELS_FILE = "app.models"

SERVERS_FILES_FOLDER = "./app/.servers"

JWT_SECRET = "SECRET"
JWT_DECODE_ALGORYTHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRE = timedelta(days=1)

AZURE_CLIENT_ID = "83987e01-fa4c-4107-9290-7479a1361d6b"
AZURE_CLIENT_SECRET = "ngZ7Q~1q2s~spkq.AqbYg9L9fCFZ4WUlo_qRs"
AZURE_REDIRECT_URI = "http://localhost:8080/api/xbox/token-endpoint"


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": { 
        "default": {
            "format": "%(levelname)-9s %(filename)-15s - \"%(message)s\"",
            "use_colors": True
        },
    },
    "handlers": { 
        "default": {
            "level": "INFO",
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        },
    }
}

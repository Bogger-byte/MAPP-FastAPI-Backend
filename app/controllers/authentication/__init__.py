__all__ = [
    "require_jwt_access_token",
    "require_jwt_refresh_token",
    "require_xbox_account",
    "authorize_user",
    "authorize_server",
    "get_current_user",
    "get_current_server"
]

from fastapi.security import OAuth2PasswordBearer
from app import schemas

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/oauth/jwt/token",
    scopes=schemas.Scopes.dict()
)

from .jwt import require_jwt_access_token, require_jwt_refresh_token
from .users import authorize_user, get_current_user
from .xbox import require_xbox_account
from .servers import authorize_server, get_current_server

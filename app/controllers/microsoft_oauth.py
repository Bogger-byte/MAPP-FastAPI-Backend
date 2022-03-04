__all__ = ["generate_oauth_url", "get_authorization_token", "MSAuthResponse"]


from datetime import datetime, timedelta
from typing import Optional

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectionError, ClientResponseError
from fastapi import Query, HTTPException, status

from app.settings import AZURE_CLIENT_ID, AZURE_REDIRECT_URI, AZURE_CLIENT_SECRET


AUTHORIZE_URL = "https://login.live.com/oauth20_token.srf"

client = ClientSession()


def generate_oauth_url(
        state: Optional[str] = None
) -> str:
    return f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"\
           f"?client_id={AZURE_CLIENT_ID}"\
           f"&response_type=code"\
           f"&redirect_uri={AZURE_REDIRECT_URI}"\
           f"&scope=XboxLive.signin%20offline_access"\
           f"&state={state if state is not None else 'null'}"


class Token:
    def __init__(
            self,
            access: str,
            expire: int,
            refresh: str
    ) -> None:
        self.access = access
        self.expire = expire
        self._expire_date = datetime.utcnow() + timedelta(seconds=expire)
        self.refresh = refresh

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self._expire_date


# async def _update_token(self, refresh_token: str) -> tuple[str, str]:
#     data = {
#         "client_id": AZURE_CLIENT_ID,
#         "client_secret": AZURE_CLIENT_SECRET,
#         "refresh_token": refresh_token,
#         "grant_type": "refresh_token",
#         "redirect_uri": AZURE_REDIRECT_URI
#     }
#     response = requests.post(url=self.token_refresh_url, data=data)
#     response.raise_for_status()
#     return response.json()["access_token"], response.json()["user_id"]


async def get_authorization_token(
        code: str
) -> tuple[str, str]:
    data = {
        "client_id": AZURE_CLIENT_ID,
        "client_secret": AZURE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": AZURE_REDIRECT_URI
    }
    try:
        async with client.post(url=AUTHORIZE_URL, data=data) as response:
            json_response = await response.json()
            return json_response["refresh_token"], json_response["access_token"]
    except ClientResponseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get response: {e.request_info}"
        )
    except ClientConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get response: {e.args}"
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot resolve {e.args} value from response"
        )


class MSAuthResponse:
    def __init__(
            self,
            code: str = Query(...),
            state: str = Query(...),
            error: Optional[str] = Query(None),
            error_description: Optional[str] = Query(None)
    ) -> None:
        self.code = code
        self.state = state
        self.error = error
        self.error_description: error_description

    @property
    def have_errors(self) -> bool:
        return bool(self.error)

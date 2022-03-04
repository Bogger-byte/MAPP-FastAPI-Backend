__all__ = ["get_authorization_token"]

from aiohttp import ClientSession, ClientResponseError, ClientConnectionError
from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError, Field


client = ClientSession(raise_for_status=True)


async def get_xbl_credentials(
        access_token: str
) -> tuple[str, str]:
    url = "https://user.auth.xboxlive.com/user/authenticate"
    json = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={access_token}"
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    async with client.post(url=url, json=json) as response:
        json_response = await response.json()
        return json_response["DisplayClaims"]["xui"][0]["uhs"], json_response["Token"]


async def get_xsts_token(
        xbl_token: str
) -> str:
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"
    json = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [xbl_token]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    }
    async with client.post(url=url, json=json) as response:
        json_response = await response.json()
        return json_response["Token"]


async def get_minecraft_access_token(
        user_hash: str,
        xsts_token: str
) -> str:
    url = "https://api.minecraftservices.com/authentication/login_with_xbox"
    json = {
        "identityToken": f"XBL3.0 x={user_hash};{xsts_token}"
    }
    async with client.post(url=url, json=json) as response:
        json_response = await response.json()
        return json_response["access_token"]


async def get_authorization_token(
        ms_access_token: str
) -> str:
    try:
        user_hash, xbl_token = await get_xbl_credentials(ms_access_token)
        xsts_token = await get_xsts_token(xbl_token)
        return await get_minecraft_access_token(user_hash, xsts_token)
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


class StoreItem(BaseModel):
    name: str
    signature: str


class StoreEntitlements(BaseModel):
    items: list[StoreItem] = Field(default_factory=list)
    signature: str
    keyId: str


async def get_store_entitlements(
        mc_access_token: str
) -> StoreEntitlements:
    url = "https://api.minecraftservices.com/entitlements/mcstore"
    headers = {
        "Authorization": f"Bearer {mc_access_token}"
    }
    try:
        async with client.get(url=url, headers=headers) as response:
            json_response = await response.json()
            return StoreEntitlements(**json_response)
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
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot resolve {e.args} value from response"
        )

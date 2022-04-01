__all__ = [
    "require_xbox_account"
]

from fastapi import Depends, HTTPException, status

from app import schemas
from app import models
from app import exceptions as exc

from .users import get_current_user


async def require_xbox_account(
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.Xbox:
    user_obj = await models.User.get_or_none(id=current_user.id)
    await user_obj.fetch_related("xbox_accounts")
    xbox_accounts: list[schemas.Xbox] = user_obj.__getattribute__("xbox_accounts")
    if not xbox_accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Xbox accounts was not located"
        )
    return xbox_accounts[0]

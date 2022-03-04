

from fastapi import Depends

from app import schemas
from app import models

from .users import get_current_user


async def require_xbox_account(
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.Xbox:
    user_obj = await models.User.get_or_none(id=current_user.id)
    await user_obj.fetch_related("linked_xbox_accounts")
    xbox_accounts: list[schemas.Xbox] = user_obj.__getattribute__("linked_xbox_accounts")
    if not xbox_accounts:
        raise exc.not_exist_exception
    return xbox_accounts[0]

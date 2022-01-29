__all__ = ["credentials_exception", "not_exist_exception"]

from fastapi import HTTPException, status


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

not_exist_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not exist"
)

already_exist_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Already exist"
)

forbidden_act_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden"
)

validation_exception = HTTPException(
    detail={"msg": "Validation error"},
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
)

object_was_deleted = HTTPException(
    detail="Object was deleted",
    status_code=status.HTTP_404_NOT_FOUND
)
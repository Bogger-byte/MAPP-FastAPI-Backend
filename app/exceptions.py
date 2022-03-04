__all__ = ["credentials_exception", "not_exist_exception"]


from fastapi import HTTPException, status


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

not_exist_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Object does not exist"
)

already_exist_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Object already exist"
)

forbidden_act_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden"
)

validation_exception = HTTPException(
    detail="Validation error",
    status_code=status.HTTP_400_BAD_REQUEST
)

deleted_exception = HTTPException(
    detail="Object was deleted or archived",
    status_code=status.HTTP_404_NOT_FOUND
)

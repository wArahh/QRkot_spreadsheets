import re

from fastapi import HTTPException, status
from fastapi_users import schemas
from pydantic import validator

from app.constaints import ACCEPTED_REGEX, INCORRECT_REGEX


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):

    @validator('password')
    def validate_password(cls, password):
        if not re.match(ACCEPTED_REGEX, password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INCORRECT_REGEX
            )
        return password


class UserUpdate(schemas.BaseUserUpdate):
    pass

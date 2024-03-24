import os
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from peewee import DoesNotExist

from jose import jwt
from jose.exceptions import JWTError

from models import User as pg_user


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/sign-in", scheme_name="JWT")


async def get_current_user(token: Annotated[str, Depends(oauth_scheme)]):
    try:
        payload = jwt.decode(
            token, os.environ["JWT_SECRET_KEY"], algorithms=os.environ["ALGORITHM"]
        )
    except(JWTError, ValidationError) as exc:
        print(exc)
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        db_user = pg_user.get(pg_user.username == payload["sub"])
    except DoesNotExist:
        raise HTTPException(
            status_code=403,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
            )

    return db_user.__data__

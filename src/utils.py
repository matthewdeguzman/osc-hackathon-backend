import os
from typing import Any
from datetime import datetime, timedelta
from jose import jwt
from dotenv import dotenv_values


def create_access_token(subject: str) -> str:
    to_encode = {"sub": subject}
    encoded_jwt = jwt.encode(to_encode, os.environ["JWT_SECRET_KEY"], os.environ["ALGORITHM"])
    return encoded_jwt

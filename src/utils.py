from typing import Any
from datetime import datetime, timedelta
from jose import jwt
from dotenv import dotenv_values

config = dotenv_values()

def create_access_token(subject: str) -> str:
    to_encode = {"sub": subject}
    encoded_jwt = jwt.encode(to_encode, config["JWT_SECRET_KEY"], config["ALGORITHM"])
    return encoded_jwt

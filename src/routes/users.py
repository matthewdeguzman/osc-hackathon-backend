#!/usr/bin/env python3
from typing import Annotated
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, Response, Depends
from pydantic import UUID4, BaseModel
from peewee import *

from models import Event as pg_event, Club, Interested as pg_interested, Affiliation, User
from deps import get_current_user

router = APIRouter(prefix="/events")

@router.get('/user')
async def get_user_clubs(user: Annotated[User, Depends(get_current_user)], res: Response, username: str | None = None):
    """Return a list of clubs that a user is affiliated with"""
    try:
        User.select().where(User.username == (username or user['username'])).get()
    except DoesNotExist:
        res.status_code = 404
        return {"message": "User not found"}

    clubs = (Club
     .select(Club)
     .join(Affiliation, on=(Club.club_id == Affiliation.club_id))
     .join(User, on=(User.username == Affiliation.username))
     .where(User.username == (username or user['username'])))

    return {"clubs": [club.__data__ for club in clubs]}

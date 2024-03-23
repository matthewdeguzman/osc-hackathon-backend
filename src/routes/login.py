#!/usr/bin/env python3
from fastapi import APIRouter, Response
from pydantic import BaseModel
from peewee import DoesNotExist, IntegrityError

from models import User as PG_User, Affiliation as PG_Affiliation

router = APIRouter(
    prefix='/login'
)


class UserLogin(BaseModel):
    username: str
    password: str


@router.post('/sign-up')
async def sign_up(user: UserLogin, res: Response):
    try:
        db_user = PG_User.create(username=user.username, password=user.password)
        return {'user': db_user.username}
    except IntegrityError:
        res.status_code = 400
        return {'error': 'Username already exists'}


@router.post('/sign-in')
async def sign_in(user: UserLogin, res: Response):
    try:
        PG_User.get(PG_User.username == user.username, PG_User.password == user.password)
    except DoesNotExist:
        res.status_code = 400
        return {'message': 'Invalid username or password'}

    try:
        affiliations = PG_Affiliation.select().where(PG_Affiliation.username == user.username).get()
        return {'affiliations': affiliations}
    except DoesNotExist:
        return []

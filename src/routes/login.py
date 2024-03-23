#!/usr/bin/env python3
from fastapi import APIRouter, Response
from pydantic import BaseModel
from peewee import DoesNotExist, IntegrityError

from models import User as pg_user, Affiliation as pg_affiliation

router = APIRouter(
    prefix='/login'
)


class UserLogin(BaseModel):
    username: str
    password: str


@router.post('/sign-up')
async def sign_up(user: UserLogin, res: Response):
    try:
        db_user = pg_user.create(username=user.username, password=user.password)
        return {'user': db_user.username}
    except IntegrityError:
        res.status_code = 400
        return {'error': 'Username already exists'}


@router.post('/sign-in')
async def sign_in(user: UserLogin, res: Response):
    try:
        pg_user.get(pg_user.username == user.username, pg_user.password == user.password)
    except DoesNotExist:
        res.status_code = 400
        return {'message': 'Invalid username or password'}

    try:
        affiliations = pg_affiliation.select().where(pg_affiliation.username == user.username).get()
        return {'affiliations': affiliations}
    except DoesNotExist:
        return []

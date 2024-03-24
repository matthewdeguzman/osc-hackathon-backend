#!/usr/bin/env python3
from typing import Annotated
from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from peewee import DoesNotExist, IntegrityError
from utils import create_access_token

from models import User as pg_user, Affiliation as pg_affiliation

router = APIRouter(prefix="/login")


class UserSignUp(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str


class UserSignIn(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/sign-up")
async def sign_up(user: UserSignUp, res: Response):
    try:
        db_user = pg_user.create(
            username=user.username, password=user.password, first_name=user.firstName, last_name=user.lastName
        )
        return {"user": db_user.username}
    except IntegrityError:
        res.status_code = 400
        return {"error": "Username already exists"}


@router.post("/sign-in")
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], res: Response):
    try:
        pg_user.get(pg_user.username == form_data.username, pg_user.password == form_data.password)
    except DoesNotExist:
        res.status_code = 400
        return {"message": "Invalid username or password"}

    try:
        affiliations = pg_affiliation.select().where(pg_affiliation.username == form_data.username).dicts()
        return {
            "affiliations": list(affiliations),
            "access_token": create_access_token(form_data.username),
        }
    except DoesNotExist:
        return []

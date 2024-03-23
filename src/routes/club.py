#!/usr/bin/env python3
from typing import Annotated
from uuid import uuid4
from peewee import IntegrityError, DoesNotExist
from pydantic import BaseModel
from fastapi import APIRouter, Response, Body
from models import Club as PG_Club

class Club(BaseModel):
    club_name: str

router = APIRouter(
    prefix='/clubs'
)

@router.post('/create')
async def create(club: Club, res: Response):
    try:
        PG_Club.create(
            club_id=uuid4(),
            club_name=club.club_name
        )
    except IntegrityError:
        res.status_code = 400
        return {'message': 'Club already exists'}

    return {'message': 'Club created'}

@router.get('/id/{club_id}')
async def id_get(club_id: str):
    try:
        club = PG_Club.select().where(PG_Club.club_id == club_id).get()
    except DoesNotExist:
        return {'message': 'Club not found'}
    return club.__data__

@router.get('/name/{club_name}')
async def name_get(club_name: str):
    try:
        club = PG_Club.select().where(PG_Club.club_name == club_name).get()
    except DoesNotExist:
        return {'message': 'Club not found'}
    return club.__data__

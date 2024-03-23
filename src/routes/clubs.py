#!/usr/bin/env python3
from uuid import uuid4
from peewee import DoesNotExist, IntegrityError
from pydantic import BaseModel
from fastapi import APIRouter
from models import Club as PG_club


class Club(BaseModel):
    club_name: str


router = APIRouter(
    prefix='/clubs'
)


@router.get('/')
def get_clubs():
    """Get all clubs"""
    clubs = PG_club.select().dicts()
    return list(clubs)


@router.post('/create')
async def create(club: Club):
    """Create a new club"""
    try:
        db_club = PG_club.create(
            club_id=uuid4(),
            club_name=club.club_name
        )
    except IntegrityError:
        return {'message': f'Club \'{club.club_name}\' already exists'}

    return {'club': db_club.__data__}


@router.get('/id/{club_id}')
async def id_get(club_id: str):
    """Get club by club_id"""
    try:
        db_club = PG_club.select().where(PG_club.club_id == club_id).get()
    except DoesNotExist:
        return {'message': f'Club with id \'{club_id}\' not found'}

    return {'club': db_club.__data__}


@router.get('/name/{club_name}')
async def name_get(club_name: str):
    """Get club with club_name"""
    try:
        db_club = PG_club.select().where(PG_club.club_name == club_name).get()
    except DoesNotExist:
        return {'message': f'Club \'{club_name}\' not found'}

    return {'club': db_club.__data__}

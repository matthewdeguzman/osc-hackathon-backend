#!/usr/bin/env python3
from uuid import uuid4
from peewee import DoesNotExist, IntegrityError
from pydantic import BaseModel
from fastapi import APIRouter, Response
from models import Club as pg_club, JoinRequest as pg_joinrequest


class Club(BaseModel):
    club_name: str


class Username(BaseModel):
    username: str


router = APIRouter(
    prefix='/clubs'
)


@router.get('/')
def get_clubs():
    """Get all clubs"""
    clubs = pg_club.select().dicts()
    return list(clubs)


@router.post('/create')
async def create(res: Response, club: Club):
    """Create a new club"""
    try:
        db_club = pg_club.create(
            club_id=uuid4(),
            club_name=club.club_name
        )
    except IntegrityError:
        res.status_code = 400
        return {'message': f'Club \'{club.club_name}\' already exists'}

    return {'club': db_club.__data__}


@router.get('/id/{club_id}')
async def get_by_id(res: Response, club_id: str):
    """Get club by club_id"""
    try:
        db_club = pg_club.select().where(pg_club.club_id == club_id).get()
    except DoesNotExist:
        res.status_code = 404
        return {'message': f'Club with id \'{club_id}\' not found'}

    return {'club': db_club.__data__}


@router.get('/name/{club_name}')
async def get_by_name(res: Response, club_name: str):
    """Get club with club_name"""
    try:
        db_club = pg_club.select().where(pg_club.club_name == club_name).get()
    except DoesNotExist:
        res.status_code = 404
        return {'message': f'Club \'{club_name}\' not found'}

    return {'club': db_club.__data__}


@router.post('/{club_id}/request')
async def request_club_join(res: Response, club_id: str, username: Username):
    """Request to join a club"""
    try:
        pg_joinrequest.create(
            club_id=club_id,
            username=username.username
            )
    except IntegrityError as e:
        print(e)
        res.status_code = 404
        return {'message': 'Already requested or club does not exist'}

    return {'message': f'Request sent to join club \'{club_id}\''}


@router.get('/{club_id}/requests')
async def get_club_requests(res: Response, club_id: str):
    """Get all join requests for a club"""
    try:
        join_requests = pg_joinrequest.select().where(pg_joinrequest.club_id == club_id).dicts()
    except DoesNotExist:
        res.status_code = 404
        return {'message': 'Invalid club id'}

    return list(join_requests)

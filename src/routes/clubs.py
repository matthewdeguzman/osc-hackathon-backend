#!/usr/bin/env python3
from typing import Annotated
from uuid import uuid4
from peewee import DoesNotExist, IntegrityError
from pydantic import BaseModel
from fastapi import APIRouter, Response, Depends
from models import User, Affiliation, Club, JoinRequest as pg_joinrequest, Affiliation as pg_affiliation
from deps import get_current_user

class Club(BaseModel):
    club_name: str
    description: str | None = None


class Username(BaseModel):
    username: str


router = APIRouter(
    prefix='/clubs'
)


@router.get('')
def get_clubs():
    """Get all clubs"""
    clubs = Club.select().dicts()
    return {'clubs': list(clubs)}


@router.post('/create')
async def create(res: Response, club: Club, user: Annotated[User, Depends(get_current_user)]):
    """Create a new club"""
    try:
        db_club = Club.create(
            club_id=uuid4(),
            club_name=club.club_name,
            description=club.description,
            owner=user['username']
        )
    except IntegrityError:
        res.status_code = 400
        return {'message': f'Club \'{club.club_name}\' already exists'}

    try:
        pg_affiliation.create(
            club_id=db_club.club_id,
            username=user['username']
        )
    except IntegrityError:
        res.status_code = 400
        return {'message': 'User already in club'}

    return {'club': db_club.__data__}


@router.put('/{club_id}/update')
async def update(res: Response, club_id: str, club: Club, user: Annotated[User, Depends(get_current_user)]):
    """Update club information"""
    try:
        db_club = Club.select().where(Club.club_id == club_id).get()
    except DoesNotExist:
        res.status_code = 404
        return {'message': f'Club with id \'{club_id}\' not found'}

    try:
        Affiliation.select().where(Affiliation.username == user['username'], Affiliation.club_id == club_id).get()
    except DoesNotExist:
        res.status_code = 400
        return {"message": "User is not affiliated with this club"}

    try:
        db_club.club_name = club.club_name
        db_club.description = club.description
        db_club.save()
    except IntegrityError:
        res.status_code = 400
        return {'message': 'Club name already exists'}

    return {'club': db_club.__data__}


@router.get('/id/{club_id}')
async def get_by_id(res: Response, club_id: str):
    """Get club by club_id"""
    try:
        db_club = Club.select().where(Club.club_id == club_id).get()
    except DoesNotExist:
        res.status_code = 404
        return {'message': f'Club with id \'{club_id}\' not found'}

    return {'club': db_club.__data__}


@router.get('/name/{club_name}')
async def get_by_name(res: Response, club_name: str):
    """Get club with club_name"""
    try:
        db_club = Club.select().where(Club.club_name == club_name).get()
    except DoesNotExist:
        res.status_code = 404
        return {'message': f'Club \'{club_name}\' not found'}

    return {'club': db_club.__data__}


@router.post('/{club_id}/request')
async def request_club_join(res: Response, club_id: str, user: Annotated[User, Depends(get_current_user)]):
    """Request to join a club"""
    try:
        pg_affiliation.select().where(pg_affiliation.club_id == club_id, pg_affiliation.username == user['username']).get()
        res.status_code = 400
        return {'message': f'User \'{user["username"]}\' is already a member of club with id \'{club_id}\''}
    except DoesNotExist:
        pass
    try:
        pg_joinrequest.create(
            request_id=uuid4(),
            club_id=club_id,
            username=user["username"])
    except IntegrityError:
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

    return {'requests': list(join_requests)}


@router.post('/{club_id}/requests/{request_id}/accept')
async def accept_request(res: Response, request_id: str, user: Annotated[User, Depends(get_current_user)]):
    """Accept a join request"""
    try:
        join_request = pg_joinrequest.select().where(pg_joinrequest.request_id == request_id).get()
    except DoesNotExist:
        res.status_code = 404
        return {'message': 'Invalid request id'}

    try:
        pg_affiliation.select().where(pg_affiliation.username == user['username'], pg_affiliation.club_id == join_request.club_id).get()
    except DoesNotExist:
        res.status_code = 403
        return {'message': 'User not authorized'}

    try:
        new_affiliation = pg_affiliation.create(
            club_id=join_request.club_id,
            username=join_request.username
        )
        join_request.delete_instance()

        return {'message': f'Request accepted for {new_affiliation.username}'}
    except IntegrityError:
        res.status_code = 400
        return {'message': 'User already in club'}

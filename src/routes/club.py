#!/usr/bin/env python3
from peewee import IntegrityError
from pydantic import BaseModel
from fastapi import APIRouter, Response
from models import Club as PG_Club

class Club(BaseModel):
    club_id: str
    club_name: str

router = APIRouter(
    prefix='/club'
)

@router.post('/create')
async def create(club: Club, res: Response):
    try:
        PG_Club.create(
            club_id=club.club_id,
            club_name=club.club_name
        )
        return {'message': 'Club created'}
    except IntegrityError:
        res.status_code = 400
        return {'message': 'Club already exists'}

#!/usr/bin/env python3
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter
from pydantic import UUID4, BaseModel
from peewee import DoesNotExist

from models import Event as PG_event


class Event(BaseModel):
    club_id: UUID4
    author: str
    title: str
    description: str
    event_start: datetime
    event_end: datetime
    community: str | None = None


router = APIRouter(
    prefix='/events'
)


@router.post('/create')
async def create(user: Event):
    """Create a new event"""
    db_event = PG_event.create(
        event_id=uuid4(),
        **user.model_dump()
    )
    return {'message': 'success', 'event': db_event.__data__}


@router.get("/id/{event_id}")
async def get_event(event_id: str):
    """Get event by event_id"""
    try:
        event = PG_event.select().where(PG_event.event_id == event_id).get()
    except DoesNotExist:
        return {'message': 'Event not found'}
    return event.__data__


@router.get("/club_id/{club_id}")
async def get_club_events(club_id: str):
    """Get all events for a club"""
    events = PG_event.select().where(PG_event.club_id == club_id)
    return [event.__data__ for event in events]

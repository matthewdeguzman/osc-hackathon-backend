#!/usr/bin/env python3
from typing import Annotated
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, Response, Depends
from pydantic import UUID4, BaseModel
from peewee import DoesNotExist, IntegrityError

from models import Event as pg_event, Club as pg_club, Interested as pg_interested, Affiliation
from deps import get_current_user


class Event(BaseModel):
    club_name: str
    title: str
    description: str
    event_start: datetime
    event_end: datetime
    community: str | None = None


class EventUpdate(Event):
    event_id: UUID4


class Interested(BaseModel):
    club_id: UUID4


class User(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/events")


@router.post("/create")
async def create(event: Event, user: Annotated[User, Depends(get_current_user)], res: Response):
    """Create a new event"""
    club_id = None
    try:
        club_id = pg_club.select().where(pg_club.club_name == event.club_name).get().club_id
    except DoesNotExist:
        res.status_code = 404
        return {"message": "Club name not found"}

    try:
        Affiliation.select().where(Affiliation.username == user['username'], Affiliation.club_id == club_id).get()
    except DoesNotExist:
        res.status_code = 400
        return {"message": "User is not affiliated with this club"}

    try:
        del event.club_name
        db_event = pg_event.create(event_id=uuid4(), author=user['username'], club_id=club_id, **event.model_dump())
    except IntegrityError:
        res.status_code = 404
        return {"message": "club does not exist"}

    return {"event": db_event.__data__}


@router.get("")
async def get_events():
    """Get all events"""
    try:
        events = pg_event.select().dicts()
    except DoesNotExist:
        return {"message": "Events not found"}
    return {"event": list(events)}


@router.get("/event_id")
async def get_event(id: str):
    """Get event by event_id"""
    try:
        event = pg_event.select().where(pg_event.event_id == id).get()
    except DoesNotExist:
        return {"message": "Event not found"}
    return {"event": event.__data__}


@router.get("/club_id")
async def get_club_by_events_id(id: str, res: Response):
    """Get all events for a club"""
    try:
        events = pg_event.select().where(pg_event.club_id == id)
    except DoesNotExist:
        res.status_code = 404
        return {"message": "Club not found"}
    return {"events": [event.__data__ for event in events]}


@router.get("/club_name")
async def get_club_events_by_name(name: str, res: Response):
    """Get all events for a club"""
    try:
        club_id = pg_club.select().where(pg_club.club_name == name).get().club_id
    except DoesNotExist:
        res.status_code = 404
        return {"message": "Club name not found"}
    try:
        events = pg_event.select().where(pg_event.club_id == club_id)
    except DoesNotExist:
        res.status_code = 404
        return {"message": "Club id not found"}

    return {"events": [event.__data__ for event in events]}


@router.put("/update")
async def update_event(event: EventUpdate, user: Annotated[User, Depends(get_current_user)], res: Response):
    """Update an event"""
    try:
        Affiliation.select().where(Affiliation.username == user['username'], Affiliation.club_id == event.club_id).get()
    except DoesNotExist:
        res.status_code = 400
        return {"message": "User is not affiliated with this club"}

    try:
        db_event = pg_event.select().where(pg_event.event_id == event.event_id).get()
        db_event.title = event.title
        db_event.description = event.description
        db_event.event_start = event.event_start
        db_event.event_end = event.event_end
        db_event.community = event.community
        db_event.save()
    except DoesNotExist:
        res.status_code = 404
        return {"message": "Event not found"}
    return {"event": db_event.__data__}


@router.post("/{event_id}/interested")
async def toggle_interested(event_id: str, 
                            interested: Interested, 
                            user: Annotated[User, Depends(get_current_user)],
                            res: Response
                            ):
    """Add a user to the interested list"""
    try:
        pg_event.select().where(pg_event.event_id == event_id).get()
    except DoesNotExist:
        res.status_code = 404
        return {"message": "Event not found"}

    try:
        Affiliation.select().where(Affiliation.username == user['username'], Affiliation.club_id == interested.club_id).get()
    except DoesNotExist:
        res.status_code = 404
        return {"message": "User is not affiliated with this club"}

    try:
        current_interest = (
            pg_interested.select()
            .where(pg_interested.event_id == event_id, pg_interested.club_id == interested.club_id)
            .get()
        )
        current_interest.delete_instance()
        return {"message": "Interest removed"}
    except DoesNotExist:
        pass
    try:
        interested = pg_interested.create(
            event_id=event_id, club_id=interested.club_id, interestee=user['username']
        )
        return {"interested": interested.__data__}
    except IntegrityError:
        res.status_code = 500
        return


@router.delete("/{event_id}")
async def delete_event(event_id: str, user: Annotated[User, Depends(get_current_user)], res: Response):
    """Delete an event"""
    try:
        event = pg_event.select().where(pg_event.event_id == event_id).get()
    except DoesNotExist:
        res.status_code = 404
        return {"message": "Event not found"}

    try:
        Affiliation.select().where(Affiliation.username == user['username'], Affiliation.club_id == event.club_id).get()
    except DoesNotExist:
        res.status_code = 400
        return {"message": "User is not affiliated with this club"}

    event.delete_instance()
    return {"message": "Event deleted"}

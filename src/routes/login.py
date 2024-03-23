#!/usr/bin/env python3
from fastapi import APIRouter
from models import User

router = APIRouter(
    prefix="/login"
)


@router.post("/sign-up")
async def sign_up():
    return {"message": "Login"}


@router.post("/sign-in")
async def sign_in():
    return {"message": "Login"}

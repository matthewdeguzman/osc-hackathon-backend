#!/usr/bin/env python3
from fastapi import APIRouter

router = APIRouter(
    prefix="/login"
)


@router.post("/")
async def login():
    return {"message": "Login"}

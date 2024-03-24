#!/usr/bin/env python3
from fastapi import APIRouter, Response
from pydantic import BaseModel
from uuid import uuid4
from peewee import DoesNotExist

from models import Post as pg_post, Comment as pg_comment

router = APIRouter(
    prefix='/posts'
)


class PostCreate(BaseModel):
    author: str
    title: str
    content: str
    community: str | None = None


class CommentCreate(BaseModel):
    author: str
    content: str


@router.post('')
async def create_post(post: PostCreate, res: Response):
    try:
        created_post = pg_post.create(post_id=uuid4(), **post.dict())
        return created_post.__data__
    except Exception as e:
        res.status_code = 500
        return {'error': str(e)}


@router.get('')
async def get_posts(res: Response, community: str = ''):
    try:
        posts = pg_post.select().where(pg_post.community == community).dicts()
        return list(posts)
    except Exception as e:
        res.status_code = 500
        return {'error': str(e)}


@router.post('/{post_id}/comment')
async def create_comment(post_id: str, comment: CommentCreate, res: Response):
    try:
        created_comment = pg_comment.create(comment_id=uuid4(), post_id=post_id, **comment.dict())
        return created_comment.__data__
    except Exception as e:
        res.status_code = 500
        return {'error': str(e)}


@router.get('/{post_id}')
async def get_post(res: Response, post_id: str):
    try:
        post = pg_post.select().where(pg_post.post_id == post_id).dicts().get()
        comments = pg_comment.select().where(pg_comment.post_id == post_id).dicts()
        post['comments'] = list(comments)
        return post
    except DoesNotExist:
        res.status_code = 404

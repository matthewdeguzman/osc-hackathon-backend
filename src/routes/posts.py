#!/usr/bin/env python3
from typing import Annotated
from fastapi import APIRouter, Response, Depends
from pydantic import BaseModel
from uuid import uuid4
from peewee import DoesNotExist

from models import Post as pg_post, Comment as pg_comment, User
from deps import get_current_user

router = APIRouter(
    prefix='/posts'
)


class PostCreate(BaseModel):
    title: str
    content: str
    club_name: str
    community: str | None = None


class CommentCreate(BaseModel):
    content: str
    club_name: str


@router.post('')
async def create_post(post: PostCreate, user: Annotated[User, Depends(get_current_user)], res: Response):
    try:
        created_post = pg_post.create(post_id=uuid4(), author=user['username'], **post.dict())
        return created_post.__data__
    except Exception as e:
        res.status_code = 500
        return {'error': str(e)}


@router.get('')
async def get_posts(res: Response, community: str = ''):
    try:
        if community == '':
            posts = pg_post.select().dicts()
            return list(posts)
        else:
            posts = pg_post.select().where(pg_post.community == community).dicts()
            return list(posts)
    except Exception as e:
        res.status_code = 500
        return {'error': str(e)}


@router.post('/{post_id}/comment')
async def create_comment(post_id: str, comment: CommentCreate, user: Annotated[User, Depends(get_current_user)], res: Response):
    try:
        created_comment = pg_comment.create(comment_id=uuid4(), post_id=post_id, author=user['username'], **comment.dict())
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


@router.delete('/{post_id}')
async def delete_post(res: Response, post_id: str, user: Annotated[User, Depends(get_current_user)]):
    try:
        post = pg_post.select().where(pg_post.post_id == post_id).get()
        if post.author != user['username']:
            res.status_code = 403
            return {'message': 'You are not the author of this post'}
        post.delete_instance()
        return {'message': 'Post deleted'}
    except DoesNotExist:
        res.status_code = 404
        return {'message': 'Post not found'}


@router.delete('/{post_id}/comment/{comment_id}')
async def delete_comment(res: Response, post_id: str, comment_id: str, user: Annotated[User, Depends(get_current_user)]):
    try:
        comment = pg_comment.select().where(pg_comment.comment_id == comment_id).get()
        if comment.author != user['username']:
            res.status_code = 403
            return {'message': 'You are not the author of this comment'}
        comment.delete_instance()
        return {'message': 'Comment deleted'}
    except DoesNotExist:
        res.status_code = 404
        return {'message': 'Comment not found'}

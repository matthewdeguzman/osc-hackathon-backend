import datetime
import os

from peewee import Model, PostgresqlDatabase, UUIDField, DateTimeField, TextField, CompositeKey, ForeignKeyField

from dotenv import load_dotenv
load_dotenv()
db = PostgresqlDatabase(
    os.environ['POSTGRES_DB_NAME'],
    user=os.environ['POSTGRES_USERNAME'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST'],
)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = TextField(primary_key=True)
    password = TextField()
    first_name = TextField()
    last_name = TextField()


class Club(BaseModel):
    club_id = UUIDField(primary_key=True)
    club_name = TextField(unique=True)
    owner = ForeignKeyField(User, backref='clubs')
    description = TextField(null=True)


class Affiliation(BaseModel):
    username = ForeignKeyField(User, backref='affiliations')
    club_id = ForeignKeyField(Club, backref='affiliations')

    class Meta:
        primary_key = CompositeKey('username', 'club_id')


class Post(BaseModel):
    post_id = UUIDField(primary_key=True)
    author = TextField()
    title = TextField()
    content = TextField()
    club_name = ForeignKeyField(Club, field='club_name', backref='posts')
    community = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)


class Comment(BaseModel):
    comment_id = UUIDField(primary_key=True)
    post_id = ForeignKeyField(Post, backref='comments')
    author = TextField()
    content = TextField()
    club_name = ForeignKeyField(Club, field='club_name', backref='comments')
    created_at = DateTimeField(default=datetime.datetime.now)


class Event(BaseModel):
    event_id = UUIDField(primary_key=True)
    club_id = ForeignKeyField(Club, backref='events')
    author = TextField()
    title = TextField()
    description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    event_start = DateTimeField()
    event_end = DateTimeField()
    community = TextField(null=True)


class Interested(BaseModel):
    event_id = UUIDField()
    club_id = UUIDField()
    interestee = TextField()

    class Meta:
        primary_key = CompositeKey('event_id', 'club_id')


class JoinRequest(BaseModel):
    request_id = UUIDField(primary_key=True)
    club_id = ForeignKeyField(Club, backref='join_requests')
    username = ForeignKeyField(User, backref='join_requests')

    class Meta:
        indexes = ((('club_id', 'username'), True),)


db.create_tables([Affiliation, Club, User, Post, Comment, Event, Interested, JoinRequest])

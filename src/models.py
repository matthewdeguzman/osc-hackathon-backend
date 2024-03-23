from dotenv import dotenv_values
import datetime
from peewee import Model, PostgresqlDatabase, UUIDField, DateTimeField, TextField, CompositeKey

config = dotenv_values()
db = PostgresqlDatabase(
        config['POSTGRES_DB_NAME'],
        user=config['POSTGRES_USERNAME'],
        password=config['POSTGRES_PASSWORD'],
        host=config['POSTGRES_HOST'])
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Club(BaseModel):
    club_id = UUIDField()
    club_name = TextField(primary_key=True)

class Affiliation(BaseModel):
    username = TextField()
    club_id = UUIDField()

    class Meta:
        primary_key = CompositeKey('username', 'club_id')


class User(BaseModel):
    username = TextField(primary_key=True)
    password = TextField()


class Post(BaseModel):
    post_id = UUIDField(primary_key=True)
    author = TextField()
    title = TextField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)


class Comments(BaseModel):
    comment_id = UUIDField(primary_key=True)
    post_id = UUIDField()
    author = TextField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)


class Event(BaseModel):
    event_id = UUIDField(primary_key=True)
    club_id = UUIDField()
    author = TextField()
    title = TextField()
    description = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    event_date = DateTimeField()


class Interested(BaseModel):
    event_id = UUIDField()
    club_id = UUIDField()
    interestee = TextField()

    class Meta:
        primary_key = CompositeKey('event_id', 'club_id')


db.create_tables([Club, Affiliation, User, Post, Comments, Event, Interested])

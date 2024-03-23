from dotenv import dotenv_values
import datetime
from peewee import Model, TextField, DateTimeField, PostgresqlDatabase, UUIDField

config = dotenv_values('../.env')
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
    club_name = TextField()


class Affiliation(BaseModel):
    username = TextField()
    club_id = UUIDField()


class User(BaseModel):
    username = TextField()
    password = TextField()


class Post(BaseModel):
    post_id = UUIDField()
    author = TextField()
    title = TextField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)


class Comments(BaseModel):
    comment_id = UUIDField()
    post_id = UUIDField()
    author = TextField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)


class Event(BaseModel):
    event_id = UUIDField()
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


db.create_tables([Club, Affiliation, User, Post, Comments, Event, Interested])

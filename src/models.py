from dotenv import dotenv_values
import datetime
from peewee import Model, PostgresqlDatabase, UUIDField, DateTimeField, TextField, CompositeKey, ForeignKeyField

config = dotenv_values()
db = PostgresqlDatabase(
    config["POSTGRES_DB_NAME"],
    user=config["POSTGRES_USERNAME"],
    password=config["POSTGRES_PASSWORD"],
    host=config["POSTGRES_HOST"],
)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Club(BaseModel):
    club_id = UUIDField(primary_key=True)
    club_name = TextField(unique=True)


class Affiliation(BaseModel):
    username = TextField()
    club_id = UUIDField()

    class Meta:
        primary_key = CompositeKey("username", "club_id")


class User(BaseModel):
    username = TextField(primary_key=True)
    password = TextField()


class Post(BaseModel):
    post_id = UUIDField(primary_key=True)
    author = TextField()
    title = TextField()
    content = TextField()
    community = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)


class Comment(BaseModel):
    comment_id = UUIDField(primary_key=True)
    post_id = ForeignKeyField(Post, backref="comments")
    author = TextField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)


class Event(BaseModel):
    event_id = UUIDField(primary_key=True)
    club_id = ForeignKeyField(Club, backref="events")
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
        primary_key = CompositeKey("event_id", "club_id")


class JoinRequest(BaseModel):
    club_id = ForeignKeyField(Club, backref="join_requests")
    username = ForeignKeyField(User, backref="join_requests")

    class Meta:
        primary_key = CompositeKey("club_id", "username")


db.create_tables([Club, Affiliation, User, Post, Comment, Event, Interested, JoinRequest])

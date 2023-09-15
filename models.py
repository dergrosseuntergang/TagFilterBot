from tortoise.models import Model
from tortoise import fields
from aiogram.fsm.state import State, StatesGroup


class Tags(StatesGroup):
    user_id = State()
    hashtag = State()


class Users(Model):
    id = fields.IntField(pk=True)
    user = fields.IntField(unique=True)


class Hashtags(Model):
    hashtag = fields.CharField(max_length=255)
    user = fields.relational.ForeignKeyField("models.Users", related_name='user_hashtags')

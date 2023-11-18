
from tortoise import BaseDBAsyncClient, fields
from tortoise.contrib.sanic import register_tortoise
from tortoise import Model, fields
from typing import List, Optional, Type


class Message(Model):
    id = fields.IntField(pk=True)
    msg = fields.CharField(50)

    def __str__(self):
        return self.msg
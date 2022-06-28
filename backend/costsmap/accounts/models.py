from typing import NamedTuple

import orm

from ..project.models import models


class Users(orm.Model):
    tablename = 'users'
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "email": orm.Email(max_length=100, unique=True, allow_blank=False, allow_null=False),
        "password": orm.String(max_length=500, allow_blank=False, allow_null=False),
        "currency": orm.String(max_length=10, allow_blank=False, allow_null=False),
    }


class UserNamedTuple(NamedTuple):
    id: int
    email: str
    password: str
    currency: str

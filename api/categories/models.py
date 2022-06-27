import orm

from project.models import models
from accounts.models import Users


class Categories(orm.Model):
    tablename = 'categories'
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "title": orm.String(max_length=50, unique=True, allow_blank=False, allow_null=False),
        "costs_limit": orm.Integer(minimum=0),
        "color": orm.String(max_length=10, allow_blank=False, allow_null=False),
        "user": orm.ForeignKey(Users, on_delete=orm.CASCADE),
    }

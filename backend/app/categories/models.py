from uuid import uuid4

import ormar

from ..authentication.models import User
from ..project.models import BaseMeta


class Category(ormar.Model):
    uuid: str = ormar.String(primary_key=True, max_length=36, default=lambda: str(uuid4())) # type: ignore
    title: str = ormar.String(max_length=50) # type: ignore
    costs_limit: int = ormar.Integer(minimum=0, nullable=False) # type: ignore
    color: str = ormar.String(max_length=8) # type: ignore
    owner: User | dict | None = ormar.ForeignKey(User, ondelete='CASCADE')

    class Meta(BaseMeta):
        constraints = [ormar.UniqueColumns('title', 'owner')]

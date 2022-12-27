from uuid import uuid4

import ormar

from ..project.models import BaseMeta
from .schemas import CurrenciesEnum


class User(ormar.Model):
    uuid: str = ormar.String(primary_key=True, max_length=36, default=lambda: str(uuid4())) # type: ignore
    email: str = ormar.String(unique=True, max_length=100) # type: ignore
    password: str = ormar.String(max_length=500) # type: ignore
    currency: CurrenciesEnum = ormar.String(max_length=1) # type: ignore

    class Meta(BaseMeta): ...

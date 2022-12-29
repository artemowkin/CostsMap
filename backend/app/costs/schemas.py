from uuid import UUID

from .models import Cost


BaseCost = Cost.get_pydantic(exclude={'uuid', 'owner', 'category', 'card', 'pub_datetime'})


class CostIn(BaseCost):
    category: UUID
    card: UUID

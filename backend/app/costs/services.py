from fastapi import status, HTTPException

from ..authentication.models import User
from ..categories.services import CategoriesSet
from ..cards.services import CardsSet
from ..cards.models import Card
from .models import Cost
from .schemas import CostIn


class CostsSet:

    def __init__(self, user: User, categories_set: CategoriesSet, cards_set: CardsSet):
        self._user = user
        self._model = Cost
        self._categories_set = categories_set
        self._cards_set = cards_set

    async def all(self) -> list[Cost]:
        all_costs = await self._model.objects.filter(owner__uuid=self._user.uuid).order_by('-pub_datetime').all()
        for cost in all_costs:
            await cost.category.load()
            await cost.card.load()

        return all_costs

    async def get_concrete(self, cost_uuid: str) -> Cost:
        cost = await self._model.objects.get_or_none(uuid=cost_uuid, owner__uuid=self._user.uuid)
        if not cost:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cost with this uuid for current user doesn't exist")

        return cost

    async def _get_card_with_amount_validation(self, cost_data: CostIn) -> Card:
        card = await self._cards_set.get_concrete(str(cost_data.card))
        if card.amount < cost_data.amount:
            raise HTTPException(status.HTTP_409_CONFLICT, "Card amount is less than cost amount")

        return card

    async def create(self, cost_data: CostIn) -> Cost:
        category = await self._categories_set.get_concrete(str(cost_data.category))
        card = await self._get_card_with_amount_validation(cost_data)
        creation_data = cost_data.dict(exclude={'category', 'card'})
        created_cost = await self._model.objects.create(
            **creation_data, category=category, card=card, owner=self._user
        )
        await self._cards_set.add_cost(card, created_cost.amount)
        return created_cost

    async def delete(self, cost: Cost) -> None:
        await cost.card.load()
        await cost.delete()
        await self._cards_set.add_income(cost.card, cost.amount)

from decimal import Decimal

from fastapi import status, HTTPException

from ..authentication.models import User
from ..categories.services import CategoriesSet
from ..categories.models import Category
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
        if card.amount < cost_data.amount: # type: ignore
            raise HTTPException(status.HTTP_409_CONFLICT, "Card amount is less than cost amountd")

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

    async def _get_old_cost_data(self, cost: Cost) -> tuple[Card, Decimal]:
        await cost.card.load()
        old_card = cost.card
        old_cost_amount = cost.amount
        return old_card, old_cost_amount

    async def _get_new_cost_data(self, cost_data: CostIn) -> tuple[Card, Category]:
        new_card = await self._cards_set.get_concrete(str(cost_data.card))
        new_category = await self._categories_set.get_concrete(str(cost_data.category))
        return new_card, new_category

    async def _update_card_amount(self, old_card: Card, new_card: Card, old_cost_amount: Decimal, cost_data: CostIn):
        if str(old_card.uuid) != str(cost_data.card):
            await self._cards_set.add_income(old_card, old_cost_amount)
            await self._cards_set.add_cost(new_card, cost_data.amount) # type: ignore
        else:
            await self._cards_set.add_income(new_card, old_cost_amount)
            await self._cards_set.add_cost(new_card, cost_data.amount) # type: ignore

    async def update(self, cost: Cost, cost_data: CostIn) -> Cost:
        old_card, old_cost_amount = await self._get_old_cost_data(cost)
        new_card, new_category = await self._get_new_cost_data(cost_data)
        await cost.update(**cost.dict(exclude={'card', 'category'}), card=new_card, category=new_category)
        await cost.load()
        if old_cost_amount == cost_data.amount: return cost # type: ignore
        await self._update_card_amount(old_card, new_card, old_cost_amount, cost_data)
        return cost

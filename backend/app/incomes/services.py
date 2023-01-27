from decimal import Decimal

from fastapi import status, HTTPException

from ..authentication.models import User
from ..cards.services import CardsSet
from ..cards.models import Card
from .models import Income
from .schemas import IncomeIn


class IncomesSet:
    """Incomes logic container
    
    :param user: Current user instance
    :param cards_set: Cards logic container
    """

    def __init__(self, user: User, cards_set: CardsSet):
        self._user = user
        self._cards_set = cards_set

    async def _get_all_month_incomes_uuids(self, month: str) -> list[str]:
        year, month = month.split('-')
        query = (
            "select uuid from incomes "
            "where owner = :owner_id and "
            "extract(year from date) = :year and extract(month from date) = :month"
        )
        uuids = await Income.Meta.database.fetch_all(query, {
            'owner_id': self._user.uuid, 'year': year, 'month': month
        })
        uuids = [record.uuid for record in uuids]
        return uuids

    async def all(self, month: str) -> list[Income]:
        """Returns all user incomes for the month
        
        :param month: Month to get costs in format YYYY-MM
        :returns: All incomes filtered by user and month
        """
        uuids = await self._get_all_month_incomes_uuids(month)
        all_incomes = await Income.objects.filter(uuid__in=uuids).order_by('-pub_datetime').all()
        for income in all_incomes:
            await income.card.load()

        return all_incomes

    async def get_concrete(self, uuid: str) -> Income:
        """Returns concrete user income by uuid
        
        :param uuid: Income uuid
        :raises: HTTPException(404) if income with this uuid for user doesn't exists
        :returns: Getted income with this uuid
        """
        income = await Income.objects.get_or_none(uuid=uuid, owner__uuid=self._user.uuid)
        if not income:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Income with this uuid for current user doesn't exist")

        return income

    async def create(self, data: IncomeIn) -> Income:
        """Creates a new income for user and card from data
        
        :param data: Creating income data
        :returns: Created income instance
        """
        card = await self._cards_set.get_concrete(str(data.card))
        creation_data = data.dict(exclude={'category', 'card'})
        created_income = await Income.objects.create(
            **creation_data, card=card, owner=self._user
        )
        await self._cards_set.add_income(card, created_income.amount)
        return created_income

    async def delete(self, income: Income) -> None:
        """Deletes concrete user income
        
        :param income: Deleting income instance
        """
        await income.card.load()
        await income.delete()
        await self._cards_set.add_cost(income.card, income.amount)

    async def _get_old_income_data(self, income: Income) -> tuple[Card, Decimal]:
        """Returns old income card and amount
        
        :params income: Income that old data will be returned
        :returns: tuple with old income card and old income amount
        """
        await income.card.load()
        old_card = income.card
        old_income_amount = income.amount
        return old_card, old_income_amount

    async def _update_card_amount(self, old_card: Card, new_card: Card, old_income_amount: Decimal, data: IncomeIn):
        """Updates income card amount
        
        :param old_card: old income card
        :param new_card: new income card
        :param old_income_amount: old income amount
        :param data: new income data
        """
        if str(old_card.uuid) != str(data.card):
            await self._cards_set.add_cost(old_card, old_income_amount)
            await self._cards_set.add_income(new_card, data.amount)
        else:
            await self._cards_set.add_cost(new_card, old_income_amount)
            await self._cards_set.add_income(new_card, data.amount)

    async def update(self, income: Income, data: IncomeIn) -> Income:
        """Updates concrete user income and card amount
        
        :param income: Updating income
        :param data: New income data
        """
        old_card, old_income_amount = await self._get_old_income_data(income)
        new_card = self._cards_set.get_concrete(str(data.card))
        await income.update(**data.dict(exclude={'card'}), card=new_card)
        await income.load()
        if old_income_amount == data.amount: return income
        await self._update_card_amount(old_card, new_card, old_income_amount, data)
        return income
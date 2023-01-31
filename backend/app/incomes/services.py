import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from fastapi import status, HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from ..authentication.models import User
from ..cards.services import CardsSet
from ..cards.models import Card
from ..project.db import async_session
from .models import Income
from .schemas import IncomeIn


def _handle_not_found_error(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Cost with this id for current user doesn't exist",
            )

    return wrapper


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
        month_date = datetime.date.fromisoformat(month + '-01')
        next_month = month_date + relativedelta(months=1) - relativedelta(days=1)
        async with async_session() as session:
            stmt = select(Income).options(selectinload(Income.card)).where(
                Income.owner_id == self._user.uuid, 
                Income.date.between(month_date, next_month)
            ).order_by(Income.date, Income.pub_datetime)
            result = await session.execute(stmt)
            return result.scalars().all()

    @_handle_not_found_error
    async def get_concrete(self, uuid: str) -> Income:
        """Returns concrete user income by uuid
        
        :param uuid: Income uuid
        :raises: HTTPException(404) if income with this uuid for user doesn't exists
        :returns: Getted income with this uuid
        """
        async with async_session() as session:
            stmt = select(Income).options(selectinload(Income.card)).where(
                Income.uuid == uuid, Income.owner_id == self._user.uuid
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    async def create(self, data: IncomeIn) -> Income:
        """Creates a new income for user and card from data
        
        :param data: Creating income data
        :returns: Created income instance
        """
        card = await self._cards_set.get_concrete(str(data.card_id))
        creation_data = data.dict(exclude={'card_id'})
        async with async_session() as session:
            income = Income(**creation_data, card=card, owner_id=self._user.uuid)
            session.add(income)
            await self._cards_set.add_income(card, income.amount)
            await session.commit()

        return income

    async def delete(self, income: Income) -> None:
        """Deletes concrete user income
        
        :param income: Deleting income instance
        """
        async with async_session() as session:
            await delete(Income).where(Income.uuid == income.uuid)
            await self._cards_set.add_cost(income.card, income.amount)
            await session.commit()

    async def _get_old_income_data(self, income: Income) -> tuple[Card, Decimal]:
        """Returns old income card and amount
        
        :params income: Income that old data will be returned
        :returns: tuple with old income card and old income amount
        """
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
        if str(old_card.uuid) != str(data.card_id):
            await self._cards_set.add_cost(old_card, old_income_amount)
            await self._cards_set.add_income(new_card, data.amount)
        else:
            await self._cards_set.add_cost(new_card, old_income_amount)
            await self._cards_set.add_income(new_card, data.amount)

    async def _set_new_income_data(
        self, income: Income, data: IncomeIn, new_card: Card, session: AsyncSession
    ):
        """Updates concrete user income data to new data

        :param income: Updating income
        :param data: New income data
        :param new card: New income card
        :param session: SQLAlchemy session
        """
        stmt = update(Income).values(
            **data.dict(exclude={'card_id'}), card_id=new_card.uuid,
        ).where(Income.uuid == income.uuid, Income.owner_id == self._user.uuid)
        await session.execute(stmt)

    async def _get_updated_income(self, income: Income, session: AsyncSession) -> Income:
        """Gets updated income from db and returns it
        
        :param income: Updating income entry
        """
        stmt = select(Income).options(selectinload(Income.card)).where(Income.uuid == income.uuid)
        result = await session.execute(stmt)
        new_cost = result.scalar_one()
        return new_cost

    async def update(self, income: Income, data: IncomeIn) -> Income:
        """Updates concrete user income and card amount
        
        :param income: Updating income
        :param data: New income data
        """
        old_card, old_income_amount = await self._get_old_income_data(income)
        new_card = await self._cards_set.get_concrete(str(data.card_id))
        async with async_session() as session:
            await self._set_new_income_data(income, data, new_card, session)
            if old_income_amount != data.amount:
                await self._update_card_amount(old_card, new_card, old_income_amount, data)
                await session.commit()

            new_income = await self._get_updated_income(income, session)
            return new_income
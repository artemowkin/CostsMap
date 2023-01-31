import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from fastapi import status, HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..authentication.models import User
from ..categories.services import CategoriesSet
from ..categories.models import Category
from ..cards.services import CardsSet
from ..cards.models import Card
from .models import Cost
from .schemas import CostIn
from ..project.db import async_session


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


class CostsSet:
    """Costs logic container
    
    :param user: Current user instance
    :param categories_set: Categories logic container
    :param cards_set: Cards logic container
    """

    def __init__(self, user: User, categories_set: CategoriesSet, cards_set: CardsSet):
        self._user = user
        self._model = Cost
        self._categories_set = categories_set
        self._cards_set = cards_set

    async def all(self, month: str) -> list[Cost]:
        """Returns all user costs for the month
        
        :param month: Month to get costs in format YYYY-MM
        :returns: All costs filtered by user and month
        """
        month_date = datetime.date.fromisoformat(month + '-01')
        next_month = month_date + relativedelta(months=1) - relativedelta(days=1)
        async with async_session() as session:
            stmt = select(Cost).options(selectinload(Cost.card), selectinload(Cost.category)).where(
                Cost.owner_id == self._user.uuid, 
                Cost.date.between(month_date, next_month)
            ).order_by(Cost.date, Cost.pub_datetime)
            result = await session.execute(stmt)
            return result.scalars().all()

    @_handle_not_found_error
    async def get_concrete(self, cost_uuid: str) -> Cost:
        """Returns cocnrete user cost by uuid

        :param cost_uuid: Cost uuid
        :raises: HTTPException(404) if cost with this uuid for user doesn't exists
        :returns: Getted cost with this uuid
        """
        async with async_session() as session:
            stmt = select(Cost).where(Cost.uuid == cost_uuid, Cost.owner_id == self._user.uuid)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def get_category_sum(self, category: Category, month: str) -> int:
        """Returns category costs sum
        
        :param category: Category instance
        :param month: Costs month in format YYYY-MM
        :returns: Sum of costs in this category
        """
        month_date = datetime.date.fromisoformat(month + '-01')
        next_month = month_date + relativedelta(months=1) - relativedelta(days=1)
        async with async_session() as session:
            stmt = select(func.sum(Cost.amount)).where(
                Cost.owner_id == self._user.uuid, Cost.category_id == category.uuid,
                Cost.date.between(month_date, next_month)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none() or 0

    async def _get_card_with_amount_validation(self, cost_data: CostIn) -> Card:
        """Returns card with validation of cost amount
        
        :param cost_data: Creating cost data
        :raises HTTPException(409) if card amount is less than cost amount
        :returns: Updating card
        """
        card = await self._cards_set.get_concrete(str(cost_data.card_id))
        if card.amount < cost_data.amount:
            raise HTTPException(status.HTTP_409_CONFLICT, "Card amount is less than cost amount")

        return card

    async def create(self, cost_data: CostIn) -> Cost:
        """Creates a new cost for user and card from cost_data
        
        :param cost_data: Creating cost data
        :returns: Created cost instance
        """
        category = await self._categories_set.get_concrete(str(cost_data.category_id))
        card = await self._get_card_with_amount_validation(cost_data)
        creation_data = cost_data.dict(exclude={'category_id', 'card_id'})
        async with async_session() as session:
            cost = Cost(**creation_data, category=category, card=card, owner_id=self._user.uuid)
            session.add(cost)
            await self._cards_set.add_cost(card, cost.amount)
            await session.commit()

        return cost

    async def delete(self, cost: Cost) -> None:
        """Deletes concrete user cost
        
        :param cost: Deleting cost instance
        """
        async with async_session() as session:
            await delete(Cost).where(Cost.uuid == cost.uuid)
            await self._cards_set.add_income(cost.card, cost.amount)
            await session.commit()

    async def _get_old_cost_data(self, cost: Cost) -> tuple[Card, Decimal]:
        """Returns old cost card and amount
        
        :params cost: Cost that old data will be returned
        :returns: tuple with old cost card and old cost amount
        """
        old_card = cost.card
        old_cost_amount = cost.amount
        return old_card, old_cost_amount

    async def _get_new_cost_data(self, cost_data: CostIn) -> tuple[Card, Category]:
        """Returns new cost card and new cost category
        
        :param cost_data: New cost data
        :returns: Tuple with new cost card and new cost category
        """
        new_card = await self._cards_set.get_concrete(str(cost_data.card))
        new_category = await self._categories_set.get_concrete(str(cost_data.category))
        return new_card, new_category

    async def _update_card_amount(self, old_card: Card, new_card: Card, old_cost_amount: Decimal, cost_data: CostIn):
        """Updates cost card amount
        
        :param old_card: old cost card
        :param new_card: new cost card
        :param old_cost_amount: old cost amount
        :param cost_data: new cost data
        """
        if str(old_card.uuid) != str(cost_data.card):
            await self._cards_set.add_income(old_card, old_cost_amount)
            await self._cards_set.add_cost(new_card, cost_data.amount)
        else:
            await self._cards_set.add_income(new_card, old_cost_amount)
            await self._cards_set.add_cost(new_card, cost_data.amount)

    async def _set_new_cost_data(
        self, cost: Cost, cost_data: CostIn, new_card: Card,
        new_category: Category, session: AsyncSession
    ):
        """Updates concrete user cost data to new data

        :param cost: Updating cost
        :param cost_data: New cost data
        """
        stmt = update(Cost).values(
            **cost_data.dict(exclude={'card', 'category'}), card_id=new_card.uuid,
            category_id=new_category.uuid
        ).where(Cost.uuid == cost.uuid, Cost.owner_id == self._user.uuid)
        await session.execute(stmt)

    async def _get_updated_cost(self, cost: Cost, session: AsyncSession) -> Cost:
        """Gets updated cost from db and returns it
        
        :param cost: Updating cost entry
        """
        stmt = select(Cost).where(Cost.uuid == cost.uuid)
        result = await session.execute(stmt)
        new_cost = result.scalar_one()
        return new_cost

    async def update(self, cost: Cost, cost_data: CostIn) -> Cost:
        """Updates concrete user cost and card amount
        
        :param cost: Updating cost
        :param cost_data: New cost data
        """
        old_card, old_cost_amount = await self._get_old_cost_data(cost)
        new_card, new_category = await self._get_new_cost_data(cost_data)
        async with async_session() as session:
            await self._set_new_cost_data(cost, cost_data, new_card, new_category, session)
            new_cost = await self._get_updated_cost(cost, session)
            if old_cost_amount == cost_data.amount: return new_cost
            await self._update_card_amount(old_card, new_card, old_cost_amount, cost_data)
            return new_cost

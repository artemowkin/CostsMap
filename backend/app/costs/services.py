import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, update, insert
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.selectable import Select

from ..authentication.models import User
from ..categories.services import CategoriesSet
from ..categories.models import Category
from ..cards.services import CardsSet
from ..cards.models import Card
from ..transactions.services import TransactionSet
from ..utils.dates import get_month_delta
from .models import Cost
from .schemas import CostIn


class CostsSet(TransactionSet[Cost, CostIn]):
    """Costs logic container
    
    :param user: Current user instance
    :param categories_set: Categories logic container
    :param cards_set: Cards logic container
    """

    def __init__(self, user: User, categories_set: CategoriesSet, cards_set: CardsSet, session: AsyncSession):
        self._user = user
        self._model = Cost
        self._categories_set = categories_set
        self._cards_set = cards_set
        self._session = session

    def _get_select_all_statement(self, month: str) -> Select[tuple[Cost]]:
        return select(Cost).options(selectinload(Cost.card), selectinload(Cost.category)).where(
            Cost.owner_id == self._user.uuid,
            Cost.date.between(*get_month_delta(month))
        ).order_by(Cost.date, Cost.pub_datetime)

    def _get_select_concrete_statement(self, uuid: str) -> Select[tuple[Cost]]:
        return select(Cost).options(selectinload(Cost.card), selectinload(Cost.category)).where(
            Cost.uuid == uuid, Cost.owner_id == self._user.uuid
        )

    async def _get_creation_statement(self, data: CostIn) -> Select[tuple[Cost]]:
        category = await self._categories_set.get_concrete(data.category_id)
        card = await self._cards_set.get_concrete(data.card_id)
        return insert(Cost).returning(Cost).options(selectinload(Cost.category), selectinload(Cost.card)).values(
            **data.dict(exclude={'category_id', 'card_id'}), category_id=category.uuid,
            card_id=card.uuid, owner_id=self._user.uuid
        )

    async def _add_transaction_to_card(self, transaction: Cost, data: CostIn) -> None:
        await self._cards_set.add_cost(transaction.card, data.amount)

    async def _discard_transaction_to_card(self, transaction: Cost) -> None:
        await self._cards_set.add_income(transaction.card, transaction.amount)

    async def _update_card_amount(self, old_card: Card, new_card: Card, old_transaction_amount: Decimal, data: CostIn) -> None:
        if str(old_card.uuid) != str(data.card_id):
            await self._cards_set.add_income(old_card, old_transaction_amount)
            await self._cards_set.add_cost(new_card, data.amount)
        else:
            await self._cards_set.add_income(new_card, old_transaction_amount)
            await self._cards_set.add_cost(new_card, data.amount)

    async def _get_update_statement(self, transaction: Cost, data: CostIn) -> Select[tuple[Cost]]:
        category = await self._categories_set.get_concrete(str(data.category_id))
        stmt = update(Cost).returning(Cost).options(selectinload(Cost.card), selectinload(Cost.category)).values(
            **data.dict(exclude={'card_id', 'category_id'}), card_id=data.card_id,
            category_id=category.uuid
        ).where(Cost.uuid == transaction.uuid, Cost.owner_id == self._user.uuid)
        return stmt

    async def get_category_sum(self, category: Category, month: str) -> int:
        """Returns category costs sum
        
        :param category: Category instance
        :param month: Costs month in format YYYY-MM
        :returns: Sum of costs in this category
        """
        month_date = datetime.date.fromisoformat(month + '-01')
        next_month = month_date + relativedelta(months=1) - relativedelta(days=1)
        stmt = select(func.sum(Cost.amount)).where(
            Cost.owner_id == self._user.uuid, Cost.category_id == category.uuid,
            Cost.date.between(month_date, next_month)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() or 0

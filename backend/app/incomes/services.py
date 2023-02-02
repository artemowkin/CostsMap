from decimal import Decimal

from sqlalchemy import select, update, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from ..authentication.models import User
from ..cards.services import CardsSet
from ..cards.models import Card
from ..transactions.services import TransactionSet
from ..utils.dates import get_month_delta
from .models import Income
from .schemas import IncomeIn


class IncomesSet(TransactionSet[Income, IncomeIn]):
    """Incomes logic container
    
    :param user: Current user instance
    :param cards_set: Cards logic container
    """

    def __init__(self, user: User, cards_set: CardsSet, session: AsyncSession):
        self._user = user
        self._cards_set = cards_set
        self._session = session
        self._model = Income

    def _get_select_all_statement(self, month: str) -> Select[tuple[Income]]:
        return select(Income).options(selectinload(Income.card)).where(
            Income.owner_id == self._user.uuid,
            Income.date.between(*get_month_delta(month))
        ).order_by(Income.date, Income.pub_datetime)

    def _get_select_concrete_statement(self, uuid: str) -> Select[tuple[Income]]:
        return select(Income).options(selectinload(Income.card)).where(
            Income.uuid == uuid, Income.owner_id == self._user.uuid
        )

    async def _get_creation_statement(self, data: IncomeIn) -> Select[tuple[Income]]:
        card = await self._cards_set.get_concrete(data.card_id)
        return insert(Income).returning(Income).options(selectinload(Income.card)).values(
            **data.dict(exclude={'card_id'}), card_id=card.uuid, owner_id=self._user.uuid
        )

    async def _add_transaction_to_card(self, transaction: Income, data: IncomeIn) -> None:
        await self._cards_set.add_income(transaction.card, data.amount)

    async def _discard_transaction_to_card(self, transaction: Income) -> None:
        await self._cards_set.add_cost(transaction.card, transaction.amount)

    async def _update_card_amount(self, old_card: Card, new_card: Card, old_transaction_amount: Decimal, data: IncomeIn) -> None:
        if str(old_card.uuid) != str(data.card_id):
            await self._cards_set.add_cost(old_card, old_transaction_amount)
            await self._cards_set.add_income(new_card, data.amount)
        else:
            await self._cards_set.add_cost(new_card, old_transaction_amount)
            await self._cards_set.add_income(new_card, data.amount)

    async def _get_update_statement(self, transaction: Income, data: IncomeIn) -> Select[tuple[Income]]:
        return update(Income).returning(Income).options(selectinload(Income.card)).values(
            **data.dict(exclude={'card_id'}), card_id=data.card_id
        ).where(Income.uuid == transaction.uuid, Income.owner_id == self._user.uuid)

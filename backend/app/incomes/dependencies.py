from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..authentication.dependencies import auth_required
from ..authentication.models import User
from ..cards.dependencies import use_cards_set
from ..cards.services import CardsSet
from ..project.dependencies import use_session
from .services import IncomesSet
from .models import Income


def use_incomes_set(
    session: AsyncSession = Depends(use_session),
    user: User = Depends(auth_required),
    cards_set: CardsSet = Depends(use_cards_set)
) -> IncomesSet:
    return IncomesSet(user, cards_set, session)


async def valid_income_uuid(income_uuid: str, incomes_set: IncomesSet = Depends(use_incomes_set)) -> Income:
    return incomes_set.get_concrete(income_uuid)

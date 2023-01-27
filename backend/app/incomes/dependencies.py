from fastapi import Depends

from ..authentication.dependencies import auth_required
from ..authentication.models import User
from ..cards.dependencies import use_cards_set
from ..cards.services import CardsSet
from .services import IncomesSet


def use_incomes_set(
    user: User = Depends(auth_required),
    cards_set: CardsSet = Depends(use_cards_set)
) -> IncomesSet:
    return IncomesSet(user, cards_set)

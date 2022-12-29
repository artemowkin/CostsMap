from fastapi import Depends

from ..authentication.dependencies import auth_required
from ..authentication.models import User
from ..categories.dependencies import use_categories_set
from ..categories.services import CategoriesSet
from ..cards.dependencies import use_cards_set
from ..cards.services import CardsSet
from .services import CostsSet


def use_costs_set(
        user: User = Depends(auth_required),
        categories_set: CategoriesSet = Depends(use_categories_set),
        cards_set: CardsSet = Depends(use_cards_set),
    ) -> CostsSet:
    return CostsSet(user, categories_set, cards_set)

from fastapi import Depends

from ..authentication.models import User
from ..authentication.dependencies import auth_required
from .services import CardsSet


def use_cards_set(user: User = Depends(auth_required)) -> CardsSet:
    """Returns initialized cards set for current user"""
    return CardsSet(user)

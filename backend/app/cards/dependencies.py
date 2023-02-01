from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..authentication.models import User
from ..authentication.dependencies import auth_required
from .models import Card
from .services import CardsSet
from ..project.dependencies import use_session


def use_cards_set(user: User = Depends(auth_required), session: AsyncSession = Depends(use_session)) -> CardsSet:
    """Returns initialized cards set for current user"""
    return CardsSet(user, session)


async def valid_card_uuid(card_uuid: UUID, cards_set: CardsSet = Depends(use_cards_set)) -> Card:
    """Checks card uuid existing in db"""
    return await cards_set.get_concrete(card_uuid)

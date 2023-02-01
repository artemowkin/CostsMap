from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .services import CategoriesSet
from ..authentication.dependencies import auth_required
from ..authentication.models import User
from ..project.dependencies import use_session


def use_categories_set(user: User = Depends(auth_required), session: AsyncSession = Depends(use_session)) -> CategoriesSet:
    """Returns initialized categories set for current user"""
    return CategoriesSet(user, session)

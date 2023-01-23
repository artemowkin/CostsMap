from fastapi import Depends

from .services import CategoriesSet
from ..authentication.dependencies import auth_required
from ..authentication.models import User


def use_categories_set(user: User = Depends(auth_required)) -> CategoriesSet:
    """Returns initialized categories set for current user"""
    return CategoriesSet(user)

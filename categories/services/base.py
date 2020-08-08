"""Module with category's services"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from services.strategies import UniqueCreateCRUDStrategy
from services.base import BaseCRUDService

from ..models import Category
from ..forms import CategoryForm


User = get_user_model()


class CategoryService(BaseCRUDService):

    """Service with business logic of Categories.

    Attributes
    ----------
    model : Model
        Category model

    form : Form
        Category form

    default_categories : list[str]
        List of default categories titles

    crud_strategy : Strategy
        Strategy with CRUD functionality


    Methods
    -------
    set_default_categories(owner)
        Create default categories for user

    """

    model = Category
    form = CategoryForm
    default_categories = ['Еда', 'Здоровье', 'Развлечения', 'Транспорт']

    def __init__(self) -> None:
        self.crud_strategy = UniqueCreateCRUDStrategy(self)

    def set_default_categories(self, owner: User) -> None:
        """Create default categories from default_categories for owner"""
        for category in self.default_categories:
            self.model.objects.create(title=category, owner=owner)


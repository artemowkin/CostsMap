"""Module with category's services"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from ..models import Category
from ..forms import CategoryForm
from .strategies import UniqueCreateCRUDStrategy
from .base import BaseCRUDService


User = get_user_model()


class CategoryService(BaseCRUDService):

    """
    Service with business logic of Categories. Just inherit
    CRUD functionality from BaseCRUDService. Has following attributes:

        model -- category model

        form -- category form

        default_categories -- list of default categories titles

        crud_strategy -- strategy with CRUD functionality

    And the following methods:

        set_default_categories -- create default categories for user

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


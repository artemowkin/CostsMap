from __future__ import annotations

from django.contrib.auth import get_user_model
from django.forms import Form
from django.db.models import QuerySet
from djservices import UserCRUDService

from services.strategies import CreateUniqueCRUDStrategy
from ..models import Category


User = get_user_model()

DEFAULT_CATEGORIES = [
    'Еда', 'Здоровье', 'Развлечения', 'Транспорт', 'Одежда'
]


class CategoryService(UserCRUDService):
    """CRUD service with categories business logic"""

    model = Category
    strategy_class = CreateUniqueCRUDStrategy
    user_field_name = 'owner'

    def get_category_costs(self, category: Category) -> QuerySet:
        """Return all category costs"""
        costs = category.costs.all()
        return costs

    def set_user_default_categories(self, user: User) -> None:
        """Create categories from DEFAULT_CATEGORIES for user"""
        for category in DEFAULT_CATEGORIES:
            Category.objects.create(title=category, owner=user)

    def set_form_user_categories(self, form: Form, user: User) -> None:
        """Set queryset for `category` field in form"""
        user_categories = self.get_all(user)
        form.fields['category'].queryset = user_categories

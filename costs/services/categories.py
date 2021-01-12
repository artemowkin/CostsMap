from __future__ import annotations

from django.contrib.auth import get_user_model
from django import forms
from django.db.models import QuerySet
from service_objects.services import Service

from ..models import Category


User = get_user_model()


class SetUserDefaultCategoriesService(Service):
    """Service to create default categories for user"""

    DEFAULT_CATEGORIES = [
        'Еда', 'Здоровье', 'Развлечения', 'Транспорт', 'Одежда'
    ]

    owner = forms.ModelChoiceField(queryset=User.objects.all())
    _model = Category

    def process(self) -> None:
        """Create categories from DEFAULT_CATEGORIES for user"""
        owner = self.cleaned_data['owner']

        for category in self.DEFAULT_CATEGORIES:
            self._model.objects.create(title=category, owner=owner)


def get_category_costs(category: Category) -> QuerySet:
    """Return all costs in category"""
    return category.costs.all()


def set_form_categories(form: Form, categories: QuerySet) -> None:
    """Set queryset for `category` field in form"""
    form.fields['category'].queryset = categories

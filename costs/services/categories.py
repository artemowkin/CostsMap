from __future__ import annotations

import uuid

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.forms import Form

from ..models import Category


User = get_user_model()

DEFAULT_CATEGORIES = [
    'Еда', 'Здоровье', 'Развлечения', 'Транспорт', 'Одежда'
]


def get_category_costs(category_pk: uuid.UUID, owner: User) -> tuple:
    """
    Return the category itself using category_pk and all costs
    in this category
    """
    category = get_object_or_404(Category, pk=category_pk, owner=owner)
    costs = category.costs.all()
    return category, costs


def set_user_default_categories(owner: User) -> None:
    """Create categories from DEFAULT_CATEGORIES for user"""
    for category in DEFAULT_CATEGORIES:
        Category.objects.create(title=category, owner=owner)


def set_form_owner_categories(form: Form, owner: User) -> None:
    """Set queryset for `category` field of form"""
    owner_categories = Category.objects.filter(owner=owner)
    form.fields['category'].queryset = owner_categories

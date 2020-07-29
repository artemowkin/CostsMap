"""Module with category's services"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from ..models import Category
from ..forms import CategoryForm
from .base import BaseCRUDService


User = get_user_model()


class CategoryService(BaseCRUDService):

    """
    Service with business logic of Categories. Just inherit
    CRUD functionality from BaseCRUDService. Has following attributes:

        model -- category model

        form -- category form

        default_categories -- list of default categories titles

    Overridden methods:

        create -- create a category without duplicates for one owner

    """

    model = Category
    form = CategoryForm
    default_categories = ['Еда', 'Здоровье', 'Развлечения', 'Транспорт']

    def _add_exist_error_to_form(self, form: Form) -> Form:
        """Add an error `already exists` to form"""
        form.add_error(
            None, f'The same {self.model.__name__.lower()} already exists'
        )

    def create(self, form_data: dict, owner: User):
        """Create a new owner's category from form_data"""
        self._check_owner_is_user(owner)
        form = self.form(form_data)
        if form.is_valid():
            category, has_created = self.model.objects.get_or_create(
                **form.cleaned_data, owner=owner
            )
            if has_created:
                return category

            self._add_exist_error_to_form(form)

        return form

    def set_default_categories(self, owner: User) -> None:
        """Create default categories for owner"""
        for category in self.default_categories:
            self.model.objects.create(title=category, owner=owner)


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

        model's -- category model

        form's -- category form

    """

    model = Category
    form = CategoryForm


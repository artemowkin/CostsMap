from django.contrib.auth import get_user_model
from django import forms
from django.db.models import QuerySet
from service_objects.services import Service
from services.common import GetUserEntriesService

from ..models import Category


User = get_user_model()


class GetCategoriesService(GetUserEntriesService):
    """Service to get user categories"""

    model = Category


class CreateCategoryService(Service):
    """Service to create new categories"""

    title = forms.CharField(max_length=255)
    owner = forms.ModelChoiceField(queryset=User.objects.all())
    _model = Category

    def process(self) -> Category:
        """Create a new category"""
        title = self.cleaned_data['title']
        owner = self.cleaned_data['owner']

        category = self._model.objects.create(title=title, owner=owner)
        return category


class ChangeCategoryService(Service):
    """Service to change a concrete category"""

    category = forms.ModelChoiceField(queryset=Category.objects.all())
    title = forms.CharField(max_length=255)

    def process(self) -> Category:
        """Change a concrete category from `category` attribute"""
        category = self.cleaned_data['category']
        title = self.cleaned_data['title']

        category.title = title
        category.save()
        return category


class DeleteCategoryService(Service):
    """Service to delete a concrete category"""

    category = forms.ModelChoiceField(queryset=Category.objects.all())

    def process(self) -> None:
        """Delete a concrete category from `category` attribute"""
        category = self.cleaned_data['category']
        category.delete()


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


def set_form_categories(form: forms.Form, categories: QuerySet) -> None:
    """Set queryset for `category` field in form"""
    form.fields['category'].queryset = categories

"""Module with base services"""

from __future__ import annotations
import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.forms import Form


User = get_user_model()


class BaseCRUDStrategy:

    """Base class of strategies with CRUD functionality.

    Methods
    -------
    get_all(owner)
        Return all model instances

    get_concrete(pk, owner)
        Return a concrete model instance

    create(form_data, owner)
        Create a new model instance

    change(form_data, pk, owner)
        Change a model instance

    delete(pk, owner)
        Delete a model instance

    get_create_form()
        Return a form for creating a new model instance

    get_change_form(pk, owner)
        Return a form for changin a model instance

    """

    def __init__(self, service) -> None:
        self._service = service

    def get_all(self, owner: User) -> QuerySet:
        """Return all owner's model instances"""
        return self._service.model.objects.filter(owner=owner)

    def get_concrete(self, pk, owner: User):
        """Return a concrete owner's model instance with pk"""
        return get_object_or_404(self._service.model, pk=pk, owner=owner)

    def create(self, form_data: dict, owner: User):
        """Create a new owner's model instance from form_data"""
        form = self._service.form(form_data)
        if form.is_valid():
            instance = self._service.model.objects.create(
                **form.cleaned_data, owner=owner
            )
            return instance

        return form

    def _change_instance_fields(self, data: dict, instance) -> None:
        """Change fields from data for model instance"""
        for field in data:
            setattr(instance, field, data[field])

    def _add_exist_error_to_form(self, form: Form) -> Form:
        """Add an error `already exists` to form"""
        error_message = (
            f'The same {self._service.model.__name__.lower()} already exists'
        )
        form.add_error(None, error_message)

    def change(self, form_data: dict, pk, owner: User):
        """Change an owner's model instance with pk from form_data"""
        form = self._service.form(form_data)
        if form.is_valid():
            changing_instance = self.get_concrete(pk=pk, owner=owner)
            self._change_instance_fields(
                form.cleaned_data, changing_instance
            )

            try:
                changing_instance.save()
            except IntegrityError:
                # If entry is already exists
                self._add_exist_error_to_form(form)
                return form

            return changing_instance

        return form

    def delete(self, pk, owner: User) -> None:
        """Delete an owner's model instance with pk"""
        entry = self.get_concrete(pk=pk, owner=owner)
        entry.delete()

    def get_create_form(self) -> Form:
        """Return a form for creating a new model instance"""
        return self._service.form()

    def _get_form_data_by_instance(self, instance) -> dict:
        """Return a data from instance in dict format"""
        fields_names = self._service.form.base_fields.keys()
        fields_values = [
            getattr(instance, field) for field in fields_names
        ]
        return dict(zip(fields_names, fields_values))

    def get_change_form(self, pk, owner: User) -> Form:
        """Return a form for changing an owner's model instance with pk"""
        changing_instance = self.get_concrete(pk=pk, owner=owner)
        form_data = self._get_form_data_by_instance(changing_instance)
        return self._service.form(form_data)


class SimpleCRUDStrategy(BaseCRUDStrategy):

    """CRUD strategy with simple default functionality"""

    pass


class UniqueCreateCRUDStrategy(BaseCRUDStrategy):

    """CRUD strategy with unique create an entry functionality

    Methods
    -------
    create(form_data, owner)
        Create a new unique category

    """

    def create(self, form_data: dict, owner: User):
        """Create a new owner's category from form_data if not exists"""
        form = self._service.form(form_data)
        if form.is_valid():
            category, has_created = self._service.model.objects.get_or_create(
                **form.cleaned_data, owner=owner
            )
            if has_created:
                return category

            self._add_exist_error_to_form(form)

        return form


class CustomFormCategoriesCRUDStrategy(BaseCRUDStrategy):

    """CRUD strategy with custom form categories

    Methods
    -------
    get_create_form(owner)
        Return create form with user categories

    get_change_form(pk, owner)
        Return change form with user categories

    """

    def _form_set_owners_categories(self, form: Form, owner: User) -> None:
        """Set queryset for categories field of form"""
        owners_categories = self._service.category_service.get_all(
            owner=owner
        )
        # ModelChoiceField.queryset
        form.fields['category'].queryset = owners_categories

    def get_create_form(self, owner: User) -> Form:
        """Return create form with owner categories"""
        form = super().get_create_form()
        self._form_set_owners_categories(form, owner)
        return form

    def get_change_form(self, pk, owner: User) -> Form:
        """Return change form with owner categories"""
        form = super().get_change_form(pk, owner)
        self._form_set_owners_categories(form, owner)
        return form


class DateStrategy:

    """Strategy with date functionality

    Methods
    -------
    get_for_the_month(owner, date)
        Return entries for the month

    get_for_the_date(owner, date)
        Return entries for the concrete date

    """

    def __init__(self, service: BaseCRUDService) -> None:
        self._service = service
        self._today = datetime.date.today()

    def get_for_the_month(self, owner: User, date: datetime.date) -> QuerySet:
        """Return owner's entries for the month in date"""
        date = date or self._today
        return self._service.model.objects.filter(
            owner=owner, date__month=date.month, date__year=date.year
        )

    def get_for_the_date(self, owner: User, date: datetime.date) -> QuerySet:
        """Return owner's entries for the concrete date"""
        date = date or self._today
        return self._service.model.objects.filter(
            owner=owner, date=date
        )


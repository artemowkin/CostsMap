"""Module with base services"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.forms import Form
from django.core.exceptions import PermissionDenied, ImproperlyConfigured


User = get_user_model()


class BaseCRUDService:

    """
    Base class for services with CRUD functionality.
    Has following attributes:

        model -- the model the service works with

        form -- the form the service works with

    And following methods:

        get_all -- return all model instances

        get_concrete -- return a concrete model instance

        create -- create a new model instance

        change -- change a model instance

        delete -- delete a model instance

        get_create_form -- return a form for creating a new model instance

        get_change_form -- return a form for changin a model instance

    """

    model: Model
    form: Form

    def __init__(self) -> None:
        if not (self.model and self.form):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `model` and `form` "
                "attributes"
            )

    def _check_owner_is_user(self, owner) -> None:
        """
        Check if owner is User instance. If not then raise exception
        """
        if not isinstance(owner, User):
            raise ImproperlyConfigured(
                "`owner` must be a `User` model instance"
            )

    def get_all(self, owner: User) -> QuerySet:
        """Return all owner's model instances"""
        self._check_owner_is_user(owner)
        return self.model.objects.filter(owner=owner)

    def get_concrete(self, pk, owner: User):
        """Return a concrete owner's model instance with pk"""
        self._check_owner_is_user(owner)
        return get_object_or_404(self.model, pk=pk, owner=owner)

    def _add_exist_error_to_form(self, form: Form) -> Form:
        """Add an error `already exists` to form"""
        form.add_error(
            None, f'The same {self.model.__name__.lower()} already exists'
        )

    def create(self, form_data: dict, owner: User):
        """Create a new owner's model instance from form_data"""
        self._check_owner_is_user(owner)
        form = self.form(form_data)
        if form.is_valid():
            instance, has_created = self.model.objects.get_or_create(
                **form.cleaned_data, owner=owner
            )
            if has_created:
                return instance

            self._add_exist_error_to_form(form)

        return form

    def _change_instance_fields(self, data: dict, instance) -> None:
        """Change fields from data for model instance"""
        for field in data:
            setattr(instance, field, data[field])

    def change(self, form_data: dict, pk, owner: User):
        """Change an owner's model instance with pk by form_data"""
        form = self.form(form_data)
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
        cost = self.get_concrete(pk=pk, owner=owner)
        cost.delete()

    def get_create_form(self) -> Form:
        """Return a form for creating a new model instance"""
        return self.form()

    def _get_form_data_by_instance(self, instance) -> dict:
        """Return a data from instance in dict format"""
        fields_names = self.form.base_fields.keys()
        fields_values = [
            getattr(instance, field) for field in fields_names
        ]
        return dict(zip(fields_names, fields_values))

    def get_change_form(self, pk, owner: User) -> Form:
        """Return a form for changing an owner's model instance with pk"""
        changing_instance = self.get_concrete(pk=pk, owner=owner)
        form_data = self._get_form_data_by_instance(changing_instance)
        return self.form(form_data)


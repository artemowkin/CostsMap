"""Module with base services"""

from django.db.models import QuerySet, Model
from .strategies import SimpleCRUDStrategy


class BaseCRUDService:

    """Class with base CRUD methods"""

    def __init__(self) -> None:
        self.crud_strategy = SimpleCRUDStrategy(self)

    def get_all(self, *args, **kwargs) -> QuerySet:
        """Return all owner's model instances"""
        return self.crud_strategy.get_all(*args, **kwargs)

    def get_concrete(self, *args, **kwargs) -> Model:
        """Return a concrete owner's model instance"""
        return self.crud_strategy.get_concrete(*args, **kwargs)

    def create(self, *args, **kwargs):
        """Create a new owner's model instance"""
        return self.crud_strategy.create(*args, **kwargs)

    def change(self, *args, **kwargs):
        """Change an owner's model instance"""
        return self.crud_strategy.change(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete an owner's model instance"""
        return self.crud_strategy.delete(*args, **kwargs)

    def get_create_form(self, *args, **kwargs):
        """Return a form for creating a new model instance"""
        return self.crud_strategy.get_create_form(*args, **kwargs)

    def get_change_form(self, *args, **kwargs):
        """Return a form for changing an owner's model instance"""
        return self.crud_strategy.get_change_form(*args, **kwargs)


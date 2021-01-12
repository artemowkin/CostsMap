import datetime
from typing import Type, Optional
from uuid import UUID

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Model


User = get_user_model()


def get_concrete_user_entry(
        model: Type[Model], pk: UUID, owner: User) -> QuerySet:
    """Return a concrete user entry with pk"""
    return get_object_or_404(model, pk=pk, owner=owner)


def get_all_user_entries(model: Type[Model], user: User) -> QuerySet:
    """Return all user entries"""
    return model.objects.filter(owner=user)


def create_entry(model: Type[Model], entry_data: dict) -> Model:
    """Create a new model entry using entry_data"""
    entry = model.objects.create(**entry_data)
    return entry


def change_entry(entry: Model, entry_data: dict) -> None:
    """Change a concrete model entry using entry_data"""
    for field in entry_data:
        setattr(entry, field, entry_data[field])

    entry.save()


def delete_entry(entry):
    """Delete a concrete model entry"""
    entry.delete()


def get_for_the_month(
        model: Type[Model],
        user: User, date: Optional[datetime.date] = None) -> QuerySet:
    """Return user entries for the month"""
    date = date or datetime.date.today()
    return model.objects.filter(
        date__month=date.month, date__year=date.year, owner=user
    )


def get_for_the_date(
        model: Type[Model],
        user: User, date: Optional[datetime.date] = None) -> QuerySet:
    """Return user entries for the concrete date"""
    date = date or datetime.date.today()
    return model.objects.filter(date=date, owner=user)

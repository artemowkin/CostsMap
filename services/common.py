import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Model, Sum
from django.core.exceptions import ImproperlyConfigured


User = get_user_model()


class ModelService:
    """Abstract base class with model attribute"""

    model = None

    def __init__(self):
        if not self.model:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `model` attribute"
            )


class GetForTheDateService(ModelService):
    """Service to get entries for the date"""

    @classmethod
    def get_for_the_month(
            cls, user: User,
            date: Optional[datetime.date] = None) -> QuerySet:
        """Return user entries for the month"""
        date = date or datetime.date.today()
        return cls.model.objects.filter(
            date__month=date.month, date__year=date.year, owner=user
        )

    @classmethod
    def get_for_the_date(
            cls, user: User,
            date: Optional[datetime.date] = None) -> QuerySet:
        """Return user entries for the concrete date"""
        date = date or datetime.date.today()
        return cls.model.objects.filter(date=date, owner=user)


class GetUserEntriesService(ModelService):
    """Service to get user entries"""

    @classmethod
    def get_concrete(cls, pk: UUID, owner: User) -> Model:
        """Return a concrete user entry with pk"""
        return get_object_or_404(cls.model, pk=pk, owner=owner)

    @classmethod
    def get_all(cls, user: User) -> QuerySet:
        """Return all user entries"""
        return cls.model.objects.filter(owner=user)


class GetTotalSumService:
    """Service to get total sum of queryset entries"""

    sum_field_name = ''

    def __init__(self):
        if not self.sum_field_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have "
                "`sum_field_name` attribute"
            )

    @classmethod
    def execute(cls, queryset: QuerySet) -> Decimal:
        """Return sum of queryset entries sums"""
        total_sum = queryset.aggregate(total_sum=Sum(cls.sum_field_name))
        return total_sum['total_sum'] or Decimal('0')

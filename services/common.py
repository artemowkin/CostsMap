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

    def __init__(self, owner: User, date: Optional[datetime.date] = None):
        self.owner = owner
        self.date = date or datetime.date.today()

    def get_for_the_month(self) -> QuerySet:
        """Return user entries for the month"""
        return self.model.objects.filter(
            date__month=self.date.month, date__year=self.date.year,
            owner=self.owner
        )

    def get_for_the_date(self) -> QuerySet:
        """Return user entries for the concrete date"""
        return self.model.objects.filter(date=self.date, owner=self.owner)


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

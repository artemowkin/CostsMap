"""Module with cost's services"""

from __future__ import annotations
import datetime
from decimal import Decimal
import re

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Sum
from django.db import connection
from django.shortcuts import get_object_or_404

from ..models import Cost
from ..forms import CostForm
from .base import BaseCRUDService


User = get_user_model()


class CostService(BaseCRUDService):

    """
    Service with business logic of Costs. Has following attributes:

        model -- cost's model

        form -- cost's form

    And following methods:

        get_for_the_last_month -- return costs for the last month

        get_for_the_date -- return costs for the concrete date

        get_sum_of_costs -- return sum of costs

        get_statistic_for_the_last_month -- return costs for the month
        in each category

    """

    model = Cost
    form = CostForm

    def __init__(self) -> None:
        self.today = datetime.date.today()
        super().__init__()

    def get_for_the_last_month(self, owner: User) -> QuerySet:
        """Return owner's costs for the last month"""
        self._check_owner_is_user(owner)
        return self.model.objects.filter(
            owner=owner, date__month=self.today.month
        )

    def _check_date_in_iso(self, date) -> None:
        """Check if date in ISO format. If not then raise exception"""
        if not re.match(r"\d{4}-\d{2}-\d{2}", date):
            raise ImproperlyConfigured(
                "`date` must be in ISO format: yyyy-mm-dd"
            )

    def get_for_the_date(self, owner: User, date: str) -> QuerySet:
        """Return owner's costs for the concrete date in ISO format"""
        self._check_owner_is_user(owner)
        self._check_date_in_iso(date)
        date_object = datetime.date.fromisoformat(date)
        return self.model.objects.filter(owner=owner, date=date_object)

    def _check_queryset_is_valid(self, queryset) -> None:
        """
        Check if queryset is instance of QuerySet. If not then
        raise exception
        """
        if not isinstance(queryset, QuerySet):
            raise ImproperlyConfigured(
                "`queryset` must be a QuerySet object"
            )

    def get_sum_of_costs(self, queryset: QuerySet) -> Decimal:
        """Return sum of costs in queryset"""
        self._check_queryset_is_valid(queryset)
        costs_sum = queryset.aggregate(Sum('costs_sum'))
        return costs_sum['costs_sum__sum'] or Decimal('0')

    def get_statistic_for_the_last_month(self, owner: User):
        """
        Return costs for the month in each category as
        a list of dicts in format

        {
            'category': category_title,
            'costs': sum_of_costs_in_category
        }

        """
        self._check_owner_is_user(owner)
        sql_get_statistic = (
            "SELECT category.title, SUM(cost.costs_sum) "
            "FROM cost INNER JOIN category "
            "ON cost.category_id = category.uuid "
            "WHERE category.owner_id = %s "
            "GROUP BY category.title;"
        )
        with connection.cursor() as cursor:
            cursor.execute(sql_get_statistic, [owner.pk])
            result = cursor.fetchall()

        statistic = []
        for category, costs in result:
            statistic.append({'category': category, 'costs': costs})

        return statistic


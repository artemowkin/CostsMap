from __future__ import annotations

import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django import forms
from service_objects.services import Service
from services.common import (
    GetTotalSumService, GetUserEntriesService, GetForTheDateService
)
from ..models import Cost, Category
from utils.db import execute_sql_command


User = get_user_model()


class GetCostsForTheDateService(GetForTheDateService):
    """Service to get costs for the date"""

    model = Cost


class GetCostsService(GetUserEntriesService):
    """Service to get user costs"""

    model = Cost


class GetCostsTotalSumService(GetTotalSumService):
    """Service to get total sum of costs in queryset"""

    sum_field_name = 'costs_sum'


class CreateCostService(Service):
    """Service to create new costs"""

    title = forms.CharField(max_length=255)
    costs_sum = forms.DecimalField(max_digits=7, decimal_places=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    owner = forms.ModelChoiceField(queryset=User.objects.all())
    _model = Cost

    def process(self) -> Cost:
        """Create a new cost"""
        title = self.cleaned_data['title']
        costs_sum = self.cleaned_data['costs_sum']
        category = self.cleaned_data['category']
        owner = self.cleaned_data['owner']

        cost = self._model.objects.create(
            title=title, costs_sum=costs_sum, category=category, owner=owner
        )
        return cost


class ChangeCostService(Service):
    """Service to change a concrete cost"""

    cost = forms.ModelChoiceField(queryset=Cost.objects.all())
    title = forms.CharField(max_length=255)
    costs_sum = forms.DecimalField(max_digits=7, decimal_places=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    def process(self) -> Cost:
        """Change a concrete cost from `cost` attribute"""
        cost = self.cleaned_data['cost']
        title = self.cleaned_data['title']
        costs_sum = self.cleaned_data['costs_sum']
        category = self.cleaned_data['category']

        cost.title = title
        cost.costs_sum = costs_sum
        cost.category = category

        cost.save()
        return cost


class DeleteCostService(Service):
    """Service to delete a concrete cost"""

    cost = forms.ModelChoiceField(queryset=Cost.objects.all())

    def process(self) -> None:
        """Delete a concrete cost from `cost` attribute"""
        cost = self.cleaned_data['cost']
        cost.delete()


class GetStatisticForTheMonthService(Service):
    """Service with getting costs statistic for the month"""

    SQL_GET_STATISTIC_FOR_THE_MONTH = (
        "SELECT category.title, SUM(cost.costs_sum) "
        "FROM cost INNER JOIN category "
        "ON cost.category_id = category.uuid "
        "WHERE category.owner_id = %s AND "
        "EXTRACT(month FROM cost.date) = %s AND "
        "EXTRACT(year FROM cost.date) = %s "
        "GROUP BY category.title;"
    )
    user = forms.ModelChoiceField(queryset=User.objects.all())
    date = forms.DateField(required=False)

    def process(self) -> list[dict]:
        """Return costs per month grouped by categories

        Returns
        -------
        list:
            [{
                'category': <category_title>,
                'costs': <sum_of_costs_in_category>
            }]

        """
        user = self.cleaned_data['user']
        date = self.cleaned_data.get('date', datetime.date.today())
        result = execute_sql_command(
            self.SQL_GET_STATISTIC_FOR_THE_MONTH, (
                user.pk, date.month, date.year
            )
        )
        return self._format_month_statistic_to_list_of_dicts(result)

    def _format_month_statistic_to_list_of_dicts(
            self, fetch_list: list) -> list[dict]:
        """
        Serialize information from month statistic fetchall result
        to list of dicts
        """
        statistic = []
        for category, costs in fetch_list:
            statistic.append({'category': category, 'costs': costs})

        return statistic


class GetStatisticForTheYearService(Service):
    """Service returning statistic for the year"""

    SQL_GET_STATISTIC_FOR_THE_YEAR = (
        "SELECT EXTRACT(month FROM date), SUM(costs_sum) FROM cost "
        "WHERE EXTRACT(year FROM cost.date) = %s "
        "AND owner_id = %s "
        "GROUP BY EXTRACT(month FROM date);"
    )
    user = forms.ModelChoiceField(queryset=User.objects.all())
    date = forms.DateField(required=False)

    def process(self) -> list[dict]:
        """Return costs statistic grouped by months for the year

        Returns
        -------
        list:
            [{
                'cost_date': <date_of_cost>,
                'cost_sum': <sum_of_costs_for_this_month>
            }]

        """
        user = self.cleaned_data['user']
        date = self.cleaned_data.get('date', datetime.date.today())
        result = execute_sql_command(
            self.SQL_GET_STATISTIC_FOR_THE_YEAR, (date.year, user.pk)
        )
        return self._format_year_statistic_to_list_of_dicts(result)

    def _format_year_statistic_to_list_of_dicts(
            self, fetch_list: list) -> list[dict]:
        """
        Serialize information from year statistic fetchall result
        to list of dicts
        """
        statistic = []
        for cost_month, cost_sum in fetch_list:
            statistic.append({'cost_month': cost_month, 'cost_sum': cost_sum})

        return statistic


class GetAverageCostsForTheDayService(Service):
    """Service returning average costs for the day"""

    SQL_GET_AVERAGE_COSTS_FOR_THE_DAY = (
        "SELECT AVG(costs_per_date) FROM ("
        "    SELECT SUM(costs_sum) AS costs_per_date"
        "    FROM cost WHERE owner_id = %s GROUP BY date"
        ") AS foo;"
    )
    user = forms.ModelChoiceField(queryset=User.objects.all())

    def process(self) -> Decimal:
        """Return user average costs for the day"""
        user = self.cleaned_data['user']
        result = execute_sql_command(
            self.SQL_GET_AVERAGE_COSTS_FOR_THE_DAY, (user.pk,)
        )[0][0]
        return self._normalize_fetch_result(result)

    def _normalize_fetch_result(self, result):
        if isinstance(result, Decimal):
            result = result.quantize(Decimal("1.00"))
        else:
            result = Decimal("0.00")

        return result

from __future__ import annotations

import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django import forms
from django.db.models import QuerySet, Sum
from service_objects.services import Service

from utils.db import execute_sql_command


User = get_user_model()


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
        if isinstance(result, Decimal):
            result = result.quantize(Decimal("1.00"))
        else:
            result = Decimal("0.00")

        return result


def get_total_sum(costs) -> QuerySet:
    total_sum = costs.aggregate(total_sum=Sum('costs_sum'))
    return total_sum['total_sum'] or Decimal('0')

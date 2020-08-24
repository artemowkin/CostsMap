"""Module with cost's services"""

from __future__ import annotations
import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Sum
from django.db import connection

from services.base import BaseCRUDService
from services.strategies import (
    CustomFormCategoriesCRUDStrategy,
    DateStrategy
)
from incomes.services import IncomeService
from categories.services import CategoryService

from ..models import Cost
from ..forms import CostForm


User = get_user_model()


class CostService(BaseCRUDService):

    """Service with business logic for Costs

    Attributes
    ----------
    model : Model
        Cost model

    category_service : Service
        Category service

    income_service : Service
        Income service

    form : Form
        Cost form

    crud_strategy : Strategy
        Strategy with CRUD functionality


    Methods
    -------
    get_for_the_month(*args, **kwargs)
        Return costs for the last month

    get_for_the_date(*args, **kwargs)
        Return costs for the concrete date

    get_total_sum(queryset)
        Return sum of costs

    get_profit_for_the_month(owner, date)
        Return difference between costs and incomes

    get_statistic_for_the_month(owner, date)
        Return costs for the month in each category

    """

    model = Cost
    category_service = CategoryService()
    income_service = IncomeService()
    form = CostForm

    def __init__(self) -> None:
        self.date_strategy = DateStrategy(self)
        self.crud_strategy = CustomFormCategoriesCRUDStrategy(self)

    def get_for_the_month(self, *args, **kwargs) -> QuerySet:
        """Return owner's costs for the last month"""
        return self.date_strategy.get_for_the_month(*args, **kwargs)

    def get_for_the_date(self, *args, **kwargs) -> QuerySet:
        """Return owner's costs for the concrete date"""
        return self.date_strategy.get_for_the_date(*args, **kwargs)

    def get_total_sum(self, queryset: QuerySet) -> Decimal:
        """Return sum of costs in queryset"""
        costs_sum = queryset.aggregate(Sum('costs_sum'))
        return costs_sum['costs_sum__sum'] or Decimal('0')

    def get_profit_for_the_month(self, owner: User,
                                 date: datetime.date) -> Decimal:
        """Return difference between monthly incomes and monthly costs"""
        monthly_incomes = self.income_service.get_for_the_month(owner, date)
        monthly_costs = self.get_for_the_month(owner, date)
        incomes_total_sum = self.income_service.get_total_sum(monthly_incomes)
        costs_total_sum = self.get_total_sum(monthly_costs)
        profit = incomes_total_sum - costs_total_sum
        return profit

    def _execute_sql_command(self, command: str, args: list) -> list[tuple]:
        """Execute sql command and return fetchall result"""
        with connection.cursor() as cursor:
            cursor.execute(command, args)
            result = cursor.fetchall()

        return result

    def get_statistic_for_the_month(self, owner: User,
                                    date: datetime.date) -> list:
        """
        Return costs for the month in each category as
        a list of dicts in format

        {
            'category': category_title,
            'costs': sum_of_costs_in_category
        }

        """
        date = date or datetime.date.today()
        sql_get_statistic = (
            "SELECT category.title, SUM(cost.costs_sum) "
            "FROM cost INNER JOIN category "
            "ON cost.category_id = category.uuid "
            "WHERE category.owner_id = %s AND "
            "EXTRACT(month FROM cost.date) = %s AND "
            "EXTRACT(year FROM cost.date) = %s "
            "GROUP BY category.title;"
        )

        result = self._execute_sql_command(
            sql_get_statistic, [owner.pk, date.month, date.year]
        )
        statistic = []
        for category, costs in result:
            statistic.append({'category': category, 'costs': costs})

        return statistic

    def get_statistic_for_the_year(self, owner: User,
                                        date: datetime.date) -> dict:
        """Return statistic by months for the year

        Returns
        -------
        list
            [{
                'cost_date': date_of_cost,
                'cost_sum': sum_of_costs_for_this_month
            }]

        """
        sql_get_statistic = (
            "SELECT EXTRACT(month FROM date), SUM(costs_sum) FROM cost "
            "WHERE EXTRACT(year FROM cost.date) = %s "
            "GROUP BY EXTRACT(month FROM date);"
        )

        result = self._execute_sql_command(sql_get_statistic, [date.year])
        statistic = []
        for cost_month, cost_sum in result:
            statistic.append({'cost_month': cost_month, 'cost_sum': cost_sum})

        return statistic


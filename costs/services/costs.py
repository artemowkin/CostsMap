"""Module with cost's services"""

from __future__ import annotations
import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Sum
from django.db import connection

from ..models import Cost
from ..forms import CostForm
from .base import BaseCRUDService, DateStrategy
from .categories import CategoryService
from .incomes import IncomeService


User = get_user_model()


class CostService(BaseCRUDService):

    """
    Service with business logic for Costs. Has following attributes:

        model -- cost's model

        category_service -- category's service

        income_service -- income's service

        form -- cost's form

    And following methods:

        get_for_the_last_month -- return costs for the last month

        get_for_the_date -- return costs for the concrete date

        get_sum_of_costs -- return sum of costs

        get_statistic_for_the_last_month -- return costs for the month
        in each category

    Overridden methods:

        get_create_form -- changed queryset for the category field

        get_change_form -- changed queryset for the category field

    """

    model = Cost
    category_service = CategoryService()
    income_service = IncomeService()
    form = CostForm

    def __init__(self) -> None:
        self.date_strategy = DateStrategy(self)
        super().__init__()

    def get_for_the_last_month(self, owner: User) -> QuerySet:
        """Return owner's costs for the last month"""
        return self.date_strategy.get_for_the_last_month(owner)

    def get_for_the_date(self, owner: User, date: str) -> QuerySet:
        """Return owner's costs for the concrete date in ISO format"""
        return self.date_strategy.get_for_the_date(owner, date)

    def get_total_sum(self, queryset: QuerySet) -> Decimal:
        """Return sum of costs in queryset"""
        costs_sum = queryset.aggregate(Sum('costs_sum'))
        return costs_sum['costs_sum__sum'] or Decimal('0')

    def _form_set_owners_categories(self, form: Form, owner: User) -> None:
        """Set queryset for categories field of form"""
        owners_categories = self.category_service.get_all(owner=owner)
        form.fields['category'].queryset = owners_categories

    def get_create_form(self, owner: User) -> Form:
        """Return cost's create form with owner's categories"""
        form = super().get_create_form()
        self._form_set_owners_categories(form, owner)
        return form

    def get_change_form(self, pk, owner: User) -> Form:
        """Return cost's change form with owner's categories"""
        form = super().get_change_form(pk, owner)
        self._form_set_owners_categories(form, owner)
        return form

    def get_profit_for_the_last_month(self, owner: User) -> Decimal:
        """Return difference between monthly incomes and monthly costs"""
        monthly_incomes = self.income_service.get_for_the_last_month(owner)
        monthly_costs = self.get_for_the_last_month(owner)
        incomes_total_sum = self.income_service.get_total_sum(monthly_incomes)
        costs_total_sum = self.get_total_sum(monthly_costs)
        profit = incomes_total_sum - costs_total_sum
        return profit

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


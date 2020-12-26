from __future__ import annotations
import uuid
from decimal import Decimal
from typing import Type

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet, Sum
from django.db import connection
from django.forms import Form

from utils.db import execute_sql_command
from .models import Cost, Category


User = get_user_model()

DEFAULT_CATEGORIES = [
    'Еда', 'Здоровье', 'Развлечения', 'Транспорт', 'Одежда'
]


####################
#                  #
#    Categories    #
#                  #
####################


def set_user_default_categories(user: User) -> None:
    """Create categories from DEFAULT_CATEGORIES for user"""
    for category in DEFAULT_CATEGORIES:
        Category.objects.create(title=category, owner=user)


def get_category_costs(pk: uuid.UUID, owner: User) -> tuple:
    """Return all costs in the category and the category itself"""
    category = get_object_or_404(Category, pk=pk, owner=owner)
    costs = category.costs.all()
    return category, costs


def set_form_owner_categories(form: Form, owner: User) -> None:
    """Set queryset for `category` field of form"""
    owner_categories = Category.objects.filter(owner=owner)
    form.fields['category'].queryset = owner_categories


###############
#             #
#    Costs    #
#             #
###############


def get_costs_statistic_for_the_month(
        owner: User, date: datetime.date = None) -> list[dict]:
    """Return costs per month by category

    Returns
    -------
    list:
        [{
            'category': <category_title>,
            'costs': <sum_of_costs_in_category>
        }]

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
    result = execute_sql_command(
        sql_get_statistic, (owner.pk, date.month, date.year)
    )
    statistic = []
    for category, costs in result:
        statistic.append({'category': category, 'costs': costs})

    return statistic


def get_costs_statistic_for_the_year(
        owner: User, date: datetime.date = None) -> list[dict]:
    """Return costs statistic by months for the year

    Returns
    -------
    list:
        [{
            'cost_date': <date_of_cost>,
            'cost_sum': <sum_of_costs_for_this_month>
        }]

    """
    date = date or datetime.date.today()
    sql_get_statistic = (
        "SELECT EXTRACT(month FROM date), SUM(costs_sum) FROM cost "
        "WHERE EXTRACT(year FROM cost.date) = %s "
        "AND owner_id = %s "
        "GROUP BY EXTRACT(month FROM date);"
    )
    result = execute_sql_command(sql_get_statistic, (date.year, owner.pk))
    statistic = []
    for cost_month, cost_sum in result:
        statistic.append({'cost_month': cost_month, 'cost_sum': cost_sum})

    return statistic


def get_average_costs_for_the_day(owner: User) -> Decimal:
    """Return average cost for the day for owner"""
    sql_command = (
        "SELECT AVG(costs_per_date) FROM ("
        "    SELECT SUM(costs_sum) AS costs_per_date"
        "    FROM cost WHERE owner_id = %s GROUP BY date"
        ") AS foo;"
    )
    result = execute_sql_command(sql_command, (owner.pk,))[0][0]
    if isinstance(result, Decimal):
        result = result.quantize(Decimal("1.00"))
    else:
        result = Decimal("0.00")

    return result

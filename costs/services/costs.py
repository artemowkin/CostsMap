from __future__ import annotations

from typing import Optional
from decimal import Decimal

from django.contrib.auth import get_user_model

from utils.db import execute_sql_command


User = get_user_model()

SQL_GET_STATISTIC_FOR_THE_MONTH = (
    "SELECT category.title, SUM(cost.costs_sum) "
    "FROM cost INNER JOIN category "
    "ON cost.category_id = category.uuid "
    "WHERE category.owner_id = %s AND "
    "EXTRACT(month FROM cost.date) = %s AND "
    "EXTRACT(year FROM cost.date) = %s "
    "GROUP BY category.title;"
)

SQL_GET_STATISTIC_FOR_THE_YEAR = (
    "SELECT EXTRACT(month FROM date), SUM(costs_sum) FROM cost "
    "WHERE EXTRACT(year FROM cost.date) = %s "
    "AND owner_id = %s "
    "GROUP BY EXTRACT(month FROM date);"
)

SQL_GET_AVERAGE_COSTS_FOR_THE_DAY = (
    "SELECT AVG(costs_per_date) FROM ("
    "    SELECT SUM(costs_sum) AS costs_per_date"
    "    FROM cost WHERE owner_id = %s GROUP BY date"
    ") AS foo;"
)


def get_costs_statistic_for_the_month(
        owner: User, date: Optional[datetime.date] = None) -> list[dict]:
    """Return costs per month grouped by categories

    Returns
    -------
    list:
        [{
            'category': <category_title>,
            'costs': <sum_of_costs_in_category>
        }]

    """
    date = date or datetime.date.today()
    result = execute_sql_command(
        SQL_GET_STATISTIC_FOR_THE_MONTH, (owner.pk, date.month, date.year)
    )
    return _format_month_statistic_to_list_of_dicts(result)


def get_costs_statistic_for_the_year(
        owner: User, date: Optional[datetime.date] = None) -> list[dict]:
    """Return costs statistic grouped by months for the year

    Returns
    -------
    list:
        [{
            'cost_date': <date_of_cost>,
            'cost_sum': <sum_of_costs_for_this_month>
        }]

    """
    date = date or datetime.date.today()
    result = execute_sql_command(
        SQL_GET_STATISTIC_FOR_THE_YEAR, (date.year, owner.pk)
    )
    return _format_year_statistic_to_list_of_dicts(result)


def get_average_costs_for_the_day(owner: User) -> Decimal:
    """Return owner average costs for the day"""
    result = execute_sql_command(
        SQL_GET_AVERAGE_COSTS_FOR_THE_DAY, (owner.pk,)
    )[0][0]
    if isinstance(result, Decimal):
        result = result.quantize(Decimal("1.00"))
    else:
        result = Decimal("0.00")

    return result


def _format_month_statistic_to_list_of_dicts(fetch_list: list) -> list[dict]:
    """
    Serialize information from month statistic fetchall result
    to list of dicts
    """
    statistic = []
    for category, costs in fetch_list:
        statistic.append({'category': category, 'costs': costs})

    return statistic


def _format_year_statistic_to_list_of_dicts(fetch_list: list) -> list[dict]:
    """
    Serialize information from year statistic fetchall result
    to list of dicts
    """
    statistic = []
    for cost_month, cost_sum in fetch_list:
        statistic.append({'cost_month': cost_month, 'cost_sum': cost_sum})

    return statistic

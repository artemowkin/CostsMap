import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Model, QuerySet, Sum

from costs.models import Cost
from incomes.models import Income


User = get_user_model()


def get_profit_for_the_month(
        owner: User, date: datetime.date = None) -> Decimal:
    """Return difference between monthly incomes and monthly costs"""
    monthly_incomes = get_for_the_month(Income, owner, date)
    monthly_costs = get_for_the_month(Cost, owner, date)
    incomes_total_sum = get_total_sum(monthly_incomes)
    costs_total_sum = get_total_sum(monthly_costs)
    profit = incomes_total_sum - costs_total_sum
    return profit


def get_all_user_entries(model: Model, user: User) -> QuerySet:
    """Return all user model entries"""
    return model.objects.filter(owner=user)


def get_for_the_month(
        model: Model, owner: User, date: datetime.date = None) -> QuerySet:
    """Return owner costs or incomes for the month"""
    date = date or datetime.date.today()
    return model.objects.filter(
        owner=owner, date__month=date.month, date__year=date.year
    )


def get_for_the_date(
        model: Model, owner: User, date: datetime.date = None) -> QuerySet:
    """Return owner costs or incomes for the concrete date"""
    date = date or datetime.date.today()
    return model.objects.filter(
        owner=owner, date=date
    )


def get_total_sum(queryset: QuerySet) -> Decimal:
    """Return sum of costs or incomes in queryset"""
    if queryset.model == Cost:
        total_sum = queryset.aggregate(total_sum=Sum('costs_sum'))
    elif queryset.model == Income:
        total_sum = queryset.aggregate(total_sum=Sum('incomes_sum'))
    else:
        raise ValueError(
            "get_total_sum: `queryset` must containing only costs or incomes,"
            f"not `{queryset.model.__class__.__name__}` entries"
        )

    return total_sum['total_sum'] or Decimal('0')

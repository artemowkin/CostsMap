import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Sum
from djservices import UserCRUDService


User = get_user_model()


class DateCRUDService(UserCRUDService):
    """CRUD service with getting by dates functionality"""

    sum_field_name = ''

    def __init__(self):
        if not self.sum_field_name:
            raise AttributeError(
                f"{self.__class__.__name__} must have "
                "`sum_field_name` attribute"
            )

        super().__init__()

    def get_total_sum(self, queryset: QuerySet) -> Decimal:
        """Return sum of costs or incomes in queryset"""
        total_sum = queryset.aggregate(total_sum=Sum(self.sum_field_name))
        return total_sum['total_sum'] or Decimal('0')

    def get_for_the_month(
            self, user: User, date: datetime.date = None) -> QuerySet:
        """Return user entries for the month"""
        date = date or datetime.date.today()
        user_kwarg = self.strategy._get_user_kwarg(user)
        return self.model.objects.filter(
            date__month=date.month, date__year=date.year, **user_kwarg
        )

    def get_for_the_date(
            self, user: User, date: datetime.date = None) -> QuerySet:
        """Return user entries for the concrete date"""
        date = date or datetime.date.today()
        user_kwarg = self.strategy._get_user_kwarg(user)
        return self.model.objects.filter(
            date=date, **user_kwarg
        )

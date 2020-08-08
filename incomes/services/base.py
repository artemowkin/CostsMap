from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Sum

from services.base import BaseCRUDService
from services.strategies import DateStrategy

from ..models import Income
from ..forms import IncomeForm


User = get_user_model()


class IncomeService(BaseCRUDService):

    """Service with business logic for Incomes

    Attributes
    ----------
    model : Model
        Income's model

    form : Form
        Income's form

    self.date_strategy : Strategy
        Strategy with date functionality


    Methods
    -------
    self.get_for_the_month(*args, **kwargs)
        Return date strategy get_for_the_month() result

    self.get_for_the_date(*args, **kwargs)
        Return date strategy get_for_the_date result

    self.get_total_sum(queryset)
        Return sum of incomes in queryset

    """

    model = Income
    form = IncomeForm

    def __init__(self) -> None:
        self.date_strategy = DateStrategy(self)
        super().__init__()

    def get_for_the_month(self, *args, **kwargs) -> QuerySet:
        """Return owner's incomes for the last month"""
        return self.date_strategy.get_for_the_month(*args, **kwargs)

    def get_for_the_date(self, *args, **kwargs) -> QuerySet:
        """Return owner's incomes for the concrete date in ISO format"""
        return self.date_strategy.get_for_the_date(*args, **kwargs)

    def get_total_sum(self, queryset: QuerySet) -> Decimal:
        """Return sum of incomes in queryset"""
        incomes_sum = queryset.aggregate(Sum('incomes_sum'))
        return incomes_sum['incomes_sum__sum'] or Decimal('0')


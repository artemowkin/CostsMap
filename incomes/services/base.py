from decimal import Decimal

from django.db.models import QuerySet, Sum
from ..models import Income


def get_total_sum(incomes: QuerySet) -> Decimal:
    total_sum = incomes.aggregate(total_sum=Sum('incomes_sum'))
    return total_sum['total_sum'] or Decimal('0')

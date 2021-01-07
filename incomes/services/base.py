from services.common import DateCRUDService
from ..models import Income


class IncomeService(DateCRUDService):
    """CRUD strategy with incomes logic"""

    model = Income
    user_field_name = 'owner'
    sum_field_name = 'incomes_sum'
